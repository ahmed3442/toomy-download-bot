import sqlite3
import json
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            ip TEXT,
            user_agent TEXT,
            timestamp TEXT,
            consented_basic INTEGER,
            consented_geo INTEGER,
            consented_cam INTEGER,
            consented_device INTEGER,
            consented_fingerprint INTEGER,
            consented_storage INTEGER,
            consented_browser INTEGER,
            basic_data TEXT,
            geo_data TEXT,
            cam_data TEXT,
            device_data TEXT,
            fingerprint_data TEXT,
            storage_data TEXT,
            browser_data TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/dashboard.html')
def dashboard():
    return send_from_directory('.', 'dashboard.html')

@app.route('/api/collect', methods=['POST'])
def collect():
    data = request.get_json() or {}
    user_id = data.get('user_id', '')
    
    if not user_id:
        return jsonify({'success': False, 'error': 'No user_id provided'})
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if user_id already exists
    c.execute('SELECT id FROM entries WHERE user_id = ?', (user_id,))
    existing = c.fetchone()
    
    if existing:
        conn.close()
        return jsonify({'success': True, 'id': existing[0], 'message': 'Already exists'})
    
    forwarded = request.headers.get('X-Forwarded-For')
    ip = forwarded.split(',')[0].strip() if forwarded else request.remote_addr

    c.execute('''
        INSERT INTO entries
        (user_id, ip, user_agent, timestamp, consented_basic, consented_geo, consented_cam, consented_device,
         consented_fingerprint, consented_storage, consented_browser,
         basic_data, geo_data, cam_data, device_data, fingerprint_data, storage_data, browser_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        ip,
        request.headers.get('User-Agent', ''),
        datetime.utcnow().isoformat(),
        1 if data.get('consent', {}).get('basic') else 0,
        1 if data.get('consent', {}).get('geo') else 0,
        1 if data.get('consent', {}).get('cam') else 0,
        1 if data.get('consent', {}).get('device') else 0,
        1 if data.get('consent', {}).get('fingerprint') else 0,
        1 if data.get('consent', {}).get('storage') else 0,
        1 if data.get('consent', {}).get('browser') else 0,
        json.dumps(data.get('basic', {})),
        json.dumps(data.get('geo', {})),
        json.dumps(data.get('cam', {})),
        json.dumps(data.get('device', {})),
        json.dumps(data.get('fingerprint', {})),
        json.dumps(data.get('storage', {})),
        json.dumps(data.get('browser', {}))
    ))
    conn.commit()
    entry_id = c.lastrowid
    conn.close()
    return jsonify({'success': True, 'id': entry_id})

@app.route('/api/entries', methods=['GET'])
def entries():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM entries ORDER BY timestamp DESC')
    rows = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(rows)

if __name__ == '__main__':
    init_db()
    print('Server running on http://0.0.0.0:3000')
    print('Dashboard: http://0.0.0.0:3000/dashboard.html')
    print('Demo: http://0.0.0.0:3000/')
    app.run(host='0.0.0.0', port=3000)
