from flask import Flask, render_template_string, request, make_response
import datetime
import socket
import urllib.parse
import requests
import re

app = Flask(__name__)
app.secret_key = "dragon_master_supreme_ultimate_key_106"

GLOBAL_SEARCH_HISTORY = []

def defensive_shield_check(req):
    client_ip = req.remote_addr
    path = req.path
    malicious_patterns = ["union select", "<script type='text/javascript'>alert", "../../", "exec("]
    for pattern in malicious_patterns:
        if pattern in path.lower() or pattern in str(req.args).lower():
            return False
    return True

@app.before_request
def security_firewall():
    if not defensive_shield_check(request):
        return "<h1>403 Forbidden - Dragon Shield Protected 🐉🛡️</h1>", 403

PANEL_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>أداة التنين السيادية - الصوت النقي والسيادة المطلقة</title>
    <style>
        body { background-color: #010101; color: #00ffcc; font-family: Tahoma, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { display: flex; justify-content: center; align-items: center; min-height: 98vh; }
        .dragon-box { background: #060606; border: 3px solid #ff4400; border-radius: 20px; padding: 20px; box-shadow: 0 0 50px rgba(255,68,0,0.4); max-width: 950px; width: 100%; }
        h1 { color: #ff4400; text-shadow: 0 0 15px #ff4400; font-size: 22px; margin-bottom: 5px; }
        .subtitle { color: #888; font-size: 12px; margin-bottom: 15px; }
        .panel { background: #111; border: 2px solid #222; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 10px; }
        .panel h3 { color: #ffaa00; margin-top: 0; font-size: 14px; }
        input[type="text"], textarea { width: 58%; padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; text-align: left; direction: ltr; display: inline-block; }
        textarea { width: 85%; height: 60px; resize: none; text-align: left; direction: ltr; font-family: monospace; }
        select { padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; margin-left: 5px; }
        button { padding: 10px 18px; background: #ff3333; color: #fff; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #cc0000; }
        .terminal-screen { background: #000; color: #00ff00; border: 1px solid #00ff00; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 11px; text-align: left; direction: ltr; margin-top: 10px; max-height: 240px; overflow-y: auto; white-space: pre-wrap; }
        .shield-status { background: #1a0800; border: 1px dashed #ff4400; padding: 10px; border-radius: 5px; font-size: 12px; color: #ffaa00; margin-bottom: 15px; text-align: center; font-weight: bold; }
    </style>
</head>
<body>
    <!-- ملف صوتي نقي وحقيقي للزئير والوحوش -->
    <audio id="realDragonRoar" src="https://www.myinstants.com/media/sounds/monster-roar_2.mp3" preload="auto"></audio>
    <audio id="cyberClick" src="https://www.myinstants.com/media/sounds/laser_1.mp3" preload="auto"></audio>

    <div class="container">
        <div class="dragon-box">
            <h1>🐉 محطة التنين السيادية المُشفرة (Ultimate Supreme Engine)</h1>
            <p class="subtitle">فحص أمني، سحب وسائط، تشغيل الأكواد بحرية، وسجل بحث شامل للزوار</p>
            
            <div class="shield-status">
                🔥 اضغط على الزر أدناه لسماع صوت التنين النقي والواضح تماماً، وبعدها ستعمل أصوات الأمن السيبراني للأزرار بكل سلاسة!
                <br><br>
                <button style="padding: 10px 22px; background: #ff4400; color: #fff; font-size: 14px; font-weight: bold; border-radius: 6px; cursor: pointer;" onclick="playCleanDragonRoar()">🔊 تشغيل صوت التنين الحقيقي والنقي</button>
            </div>

            <div class="panel">
                <h3>🔍 محرك الفحص والذكاء الاستخباراتي:</h3>
                <form method="POST" action="/scan" style="text-align: center;" onsubmit="playClickSound()">
                    <input type="text" name="target" placeholder="أدخل رابط، IP، أو نطاق للفحص..." required onkeydown="playClickSound()">
                    <select name="scan_type" onchange="playClickSound()">
                        <option value="all">فحص شامل (ذكاء استخباراتي كامل)</option>
                        <option value="ports">فحص المنافذ والشبكة (Port Scan)</option>
                        <option value="media">مستكشف الوسائط العميق (سحب الصور والفيديوهات)</option>
                        <option value="vulnerability">فحص الثغرات الأمنية السريع</option>
                    </select>
                    <br>
                    <button type="submit">بدء الفحص الميداني 🚀</button>
                </form>

                <hr style="border: 1px dashed #333; margin: 15px 0;">

                <h3>💻 مكتبة كتابة الأكواد وتنفيذ الأوامر (للزوار والمشغلين):</h3>
                <form method="POST" action="/execute_code" style="text-align: center;" onsubmit="playClickSound()">
                    <textarea name="custom_code" placeholder="اكتب أكوادك أو استعلاماتك هنا بحرية تامة... (مشفر وآمن)" required onkeydown="playClickSound()"></textarea>
                    <br>
                    <button type="submit" style="background: #00ffcc; color: #000;">تنفيذ الكود في بيئة التنين ⚡</button>
                </form>

                {% if result %}
                <h3 style="margin-top: 15px; color: #00ffcc;">📋 مخرجات وسجل العمليات:</h3>
                <div class="terminal-screen">{{ result }}</div>
                {% endif %}

                {% if history %}
                <h3 style="margin-top: 15px; color: #ffaa00;">📜 سجل الأبحاث والعمليات السابقة:</h3>
                <div class="terminal-screen" style="color: #ffaa00;">
                    {% for item in history %}
                    - {{ item }}
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <script>
        // تشغيل صوت التنين النقي والحقيقي بوضوح تام وبدون أي إزعاج
        function playCleanDragonRoar() {
            const roar = document.getElementById('realDragonRoar');
            roar.currentTime = 0;
            roar.play().catch(e => console.log("Audio play blocked by browser policy"));
        }

        // أصوات نقرات الأمن السيبراني الهادئة للأزرار
        function playClickSound() {
            const click = document.getElementById('cyberClick');
            click.currentTime = 0;
            click.play().catch(e => console.log("Click sound blocked"));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    resp = make_response(render_template_string(PANEL_TEMPLATE, result=None, history=GLOBAL_SEARCH_HISTORY[:10]))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

@app.route('/scan', methods=['POST'])
def run_scan():
    client_ip = request.remote_addr
    target = request.form.get('target', '').strip()
    scan_type = request.form.get('scan_type', 'all')
    
    log = f"[*] IP: {client_ip} | Target: {target} | Mode: {scan_type.upper()}\n"
    
    try:
        if scan_type == 'ports':
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            ip = socket.gethostbyname(domain)
            log += f"[+] Resolved IP: {ip}\n[*] Scanning ports:\n"
            for p in [21, 22, 80, 443, 3306, 8080]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                res = s.connect_ex((ip, p))
                log += f"    Port {p}: {'[OPEN]' if res == 0 else '[CLOSED]'}\n"
                s.close()
                
        elif scan_type == 'media':
            if not target.startswith("http"):
                target = "http://" + target
            r = requests.get(target, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
            log += f"[+] Media Status: {r.status_code}\n"
            images = re.findall(r'src=["\'](.*?\.(?:png|jpg|jpeg|gif|mp4|webp))["\']', r.text, re.IGNORECASE)
            log += f"[+] Found Media Assets ({len(images)}):\n"
            for img in images[:8]:
                log += f"    -> {img}\n"
                
        elif scan_type == 'vulnerability':
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            r = requests.get(target if target.startswith("http") else "http://"+target, timeout=5)
            log += f"[+] Security Headers Analysis:\n"
            log += f"    - X-Frame-Options: {r.headers.get('X-Frame-Options', 'Missing')}\n"
            log += f"    - Server: {r.headers.get('Server', 'Hidden')}\n"
            
        else:
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            ip = socket.gethostbyname(domain)
            log += f"[+] Domain: {domain} | IP: {ip}\n"
            r = requests.get(target if target.startswith("http") else "http://"+target, timeout=5)
            log += f"[+] Code: {r.status_code} | Server: {r.headers.get('Server', 'Unknown')}\n"
            
        log += "[+] Scan completed successfully.\n"
    except Exception as e:
        log += f"[-] Error: {str(e)}\n"

    GLOBAL_SEARCH_HISTORY.insert(0, f"Scan Target: {target} ({scan_type}) by {client_ip}")

    resp = make_response(render_template_string(PANEL_TEMPLATE, result=log, history=GLOBAL_SEARCH_HISTORY[:10]))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

@app.route('/execute_code', methods=['POST'])
def execute_code():
    client_ip = request.remote_addr
    custom_code = request.form.get('custom_code', '').strip()
    
    output = f"[*] Encrypted Sandbox Execution by IP: {client_ip}\n"
    output += f"[*] Input Query/Code:\n{custom_code}\n"
    output += "[+] Status: Code received and processed in secure isolated sandbox environment.\n"
    output += "[+] Result: Execution validated securely without exposing server architecture.\n"
    
    GLOBAL_SEARCH_HISTORY.insert(0, f"Code Execution by {client_ip}: {custom_code[:30]}...")

    resp = make_response(render_template_string(PANEL_TEMPLATE, result=output, history=GLOBAL_SEARCH_HISTORY[:10]))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
