with open('/home/ahmed/Desktop/New Folder/index.html', 'w', encoding='utf-8') as f:
    f.write(r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Privacy Demo</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Tahoma,sans-serif; background:#0f0f1a; color:#e0e0e0; min-height:100vh; padding:2rem 1rem; }
.container { max-width:800px; margin:0 auto; }
h1 { text-align:center; color:#ff6b6b; margin-bottom:0.5rem; }
.subtitle { text-align:center; color:#888; margin-bottom:2rem; }
.info-link { text-align:center; color:#4ecdc4; cursor:pointer; margin-bottom:1.5rem; text-decoration:underline; font-size:0.95rem; }
.info-box { display:none; background:#1a1a2e; border:1px solid #333; border-radius:12px; padding:1.25rem; margin-bottom:1.5rem; }
.info-box h4 { color:#4ecdc4; margin-bottom:0.5rem; }
.info-box ul { list-style:none; }
.info-box li { padding:0.3rem 0; color:#ccc; font-size:0.9rem; }
.btn { width:100%; padding:1.2rem; border:none; border-radius:12px; font-size:1.2rem; cursor:pointer; transition:0.3s; }
.btn-primary { background:#ff6b6b; color:#fff; }
.btn-primary:hover { background:#ff5252; }
.btn-primary:disabled { background:#333; color:#666; cursor:not-allowed; }
.results { display:none; background:#1a1a2e; border-radius:12px; padding:1.5rem; margin-top:2rem; border:1px solid #4ecdc4; }
.results h2 { color:#4ecdc4; margin-bottom:1rem; }
.data-card { background:#0f0f1a; border-radius:8px; padding:1rem; margin-bottom:0.75rem; }
.data-card h4 { color:#ff6b6b; margin-bottom:0.5rem; }
.data-card p { color:#ccc; word-break:break-all; font-size:0.9rem; }
.status-msg { text-align:center; margin-top:1rem; font-size:1rem; }
.warning-box { background:rgba(255,107,107,0.1); border:1px solid #ff6b6b; border-radius:12px; padding:1rem; margin-bottom:1.5rem; font-size:0.85rem; }
.warning-box strong { color:#ff6b6b; }
</style>
</head>
<body>
<div class="container">
<h1>Privacy Awareness Demo</h1>
<p class="subtitle">اعرف إيه المعلومات اللي المواقع ممكن تجمعها عن جهازك</p>
<div class="warning-box"><strong>تنبيه:</strong> ده educational demo. اضغط الزرار هتلاقي البيانات اللي اتجمعت ظهرت قدامك، واتبعتت للسيرفر عشان تشوفها في الـ Dashboard.</div>
<div class="info-link" onclick="toggleInfo()">لمعرفة المعلومات التي سيتم جمعها اضغط هنا</div>
<div class="info-box" id="infoBox">
<h4>المعلومات التي سيتم جمعها:</h4>
<ul>
<li>User-Agent (نوع المتصفح والجهاز)</li>
<li>IP Address (عنوان الشبكة)</li>
<li>اللغة والمنطقة الزمنية</li>
<li>أبعاد الشاشة</li>
<li>الموقع الجغرافي (GPS) — هيطلب إذنك</li>
<li>عدد الكاميرات والمايكات المتصلة</li>
<li>CPU cores, Battery level, Connection type</li>
</ul>
</div>
<button class="btn btn-primary" id="mainBtn" onclick="runCollection()">جمع المعلومات وإرسالها للسيرفر</button>
<div class="status-msg" id="statusMsg"></div>
<div class="results" id="results">
<h2>النتائج — ده اللي اتجمع واتبعت</h2>
<div id="resultsContainer"></div>
</div>
</div>
<script>
function toggleInfo(){var b=document.getElementById("infoBox");b.style.display=b.style.display==="block"?"none":"block";}
function setStatus(t,c){var e=document.getElementById("statusMsg");e.textContent=t;e.style.color=c||"#4ecdc4";}
function renderCard(t,d){var c=document.getElementById("resultsContainer");var x=document.createElement("div");x.className="data-card";var h="<h4>"+t+"</h4>";for(var k in d){h+="<p><strong>"+k+":</strong> "+d[k]+"</p>";}x.innerHTML=h;c.appendChild(x);}
async function runCollection(){
var btn=document.getElementById("mainBtn");btn.disabled=true;setStatus("جاري جمع المعلومات...","#4ecdc4");
document.getElementById("resultsContainer").innerHTML="";document.getElementById("results").style.display="block";
var col={basic:{},geo:{},cam:{},device:{}};var con={basic:true,geo:true,cam:true,device:true};
var nav=navigator;var sc=window.screen;
col.basic={"User-Agent":nav.userAgent,Language:nav.language,Platform:nav.platform,Screen:sc.width+"x"+sc.height,Viewport:window.innerWidth+"x"+window.innerHeight,Timezone:Intl.DateTimeFormat().resolvedOptions().timeZone};
try{var r=await fetch("https://api.ipify.org?format=json");var d=await r.json();col.basic["IP Address"]=d.ip;}catch(e){col.basic["IP Address"]="Failed";}
renderCard("المعلومات الأساسية",col.basic);
col.cam={};
if("mediaDevices"in navigator){try{var dev=await navigator.mediaDevices.enumerateDevices();var cam=dev.filter(function(x){return x.kind==="videoinput";});var mic=dev.filter(function(x){return x.kind==="audioinput";});col.cam={"Cameras detected":cam.length,"Microphones detected":mic.length};}catch(e){col.cam={Error:"Permission denied"};}}else{col.cam={Error:"MediaDevices not available"};}
renderCard("الكاميرا والمايك",col.cam);
col.device={"CPU Cores":nav.hardwareConcurrency||"N/A","Device Memory":nav.deviceMemory?nav.deviceMemory+" GB":"N/A","Connection Type":nav.connection?nav.connection.effectiveType:"N/A",Online:nav.onLine,"Cookies Enabled":nav.cookieEnabled,"Touch Support":"ontouchstart"in window?"Yes":"No"};
if("getBattery"in nav){try{var bat=await nav.getBattery();col.device["Battery Level"]=(bat.level*100).toFixed(0)+"%";col.device["Battery Charging"]=bat.charging?"Yes":"No";}catch(e){}}
renderCard("معلومات الجهاز",col.device);
setStatus("بيتم طلب الموقع الجغرافي (انتظر الإذن)...","#ff6b6b");
var geoDone=false;
if("geolocation"in navigator){
var gp=new Promise(function(r){navigator.geolocation.getCurrentPosition(function(p){col.geo={Latitude:p.coords.latitude,Longitude:p.coords.longitude,Accuracy:p.coords.accuracy+" meters"};geoDone=true;r();},function(e){col.geo={Error:e.message};r();},{timeout:10000});});
await Promise.race([gp,new Promise(function(r){setTimeout(r,5000);})]);
if(!geoDone&&Object.keys(col.geo).length===0)col.geo={Status:"Waiting for permission..."};
}else{col.geo={Error:"Not supported"};}
renderCard("الموقع الجغرافي",col.geo);
setStatus("بيتم الإرسال للسيرفر...","#4ecdc4");
try{var res=await fetch("/api/collect",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({consent:con,basic:col.basic,geo:col.geo,cam:col.cam,device:col.device})});var data=await res.json();if(data.success){setStatus("تم الإرسال! شوف Dashboard: /dashboard.html","#4ecdc4");}else{setStatus("فشل في الإرسال","#ff6b6b");}}catch(e){setStatus("خطأ في الإرسال: تأكد إن السيرفر شغال","#ff6b6b");}
btn.disabled=false;
}
</script>
</body>
</html>""")
print('Done')
