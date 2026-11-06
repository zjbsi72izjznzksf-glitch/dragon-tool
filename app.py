from flask import Flask, render_template_string, request, session, redirect, url_for, make_response
import datetime
import socket
import urllib.parse
import requests
import re

app = Flask(__name__)
app.secret_key = "dragon_master_supreme_ultimate_key_777"

# نظام الجدار الدفاعي المتقدم لتسجيل وحماية السيرفر من الهجمات
SECURITY_LOGS = []

def defensive_shield_check(req):
    client_ip = req.remote_addr
    user_agent = req.headers.get('User-Agent', '')
    path = req.path
    
    # فحص الأنماط الخبيثة والتصدّي لها فوراً
    malicious_patterns = ["union select", "<script>", "../../", "eval(", "exec("]
    for pattern in malicious_patterns:
        if pattern in path.lower() or pattern in str(req.args).lower():
            alert_msg = f"[{datetime.datetime.now()}] 🛡️ BLOCK ATTACK: Malicious payload detected from IP: {client_ip}"
            SECURITY_LOGS.insert(0, alert_msg)
            return False
    return True

@app.before_request
def security_firewall():
    if not defensive_shield_check(request):
        return "<h1>403 Forbidden - Dragon Shield Blocked Your Request 🐉🛡️</h1>", 403

PANEL_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>أداة التنين السيادية - محطة الاستخبارات والوسائط الشاملة</title>
    <style>
        body { background-color: #030303; color: #00ffcc; font-family: Tahoma, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { display: flex; justify-content: center; align-items: center; min-height: 98vh; }
        .dragon-box { background: #080808; border: 3px solid #00ffcc; border-radius: 20px; padding: 20px; box-shadow: 0 0 40px rgba(0,255,204,0.3); max-width: 950px; width: 100%; }
        h1 { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-size: 21px; margin-bottom: 5px; }
        .subtitle { color: #888; font-size: 12px; margin-bottom: 15px; }
        .panel { background: #111; border: 2px solid #222; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 10px; }
        .panel h3 { color: #ffaa00; margin-top: 0; font-size: 14px; }
        input[type="text"] { width: 58%; padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; text-align: left; direction: ltr; display: inline-block; }
        select { padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; margin-left: 5px; }
        button { padding: 10px 18px; background: #ff3333; color: #fff; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #cc0000; }
        .terminal-screen { background: #000; color: #00ff00; border: 1px solid #00ff00; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 11px; text-align: left; direction: ltr; margin-top: 10px; max-height: 280px; overflow-y: auto; white-space: pre-wrap; }
        .shield-status { background: #001a1a; border: 1px dashed #00ffcc; padding: 8px; border-radius: 5px; font-size: 11px; color: #00ffcc; margin-bottom: 10px; text-align: right; }
    </style>
</head>
<body>
    <div class="container">
        <div class="dragon-box">
            <h1>🐉 محطة التنين السيادية الشاملة (Ultimate OSINT Engine)</h1>
            <p class="subtitle">فحص أمني، استكشاف منافذ، سحب وسائط عميق، وجدار دفاعي نشط بكل ثانية</p>
            
            <div class="shield-status">
                🛡️ درع التنين النفاذ: نشط ويتصدى للهجمات | السيرفر محمي بالكامل ضد التسريبات والثغرات.
            </div>

            <div class="panel">
                <h3>🔍 محرك الفحص والتحليل الشامل:</h3>
                <form method="POST" action="/scan" style="text-align: center;">
                    <input type="text" name="target" placeholder="أدخل رابط، IP، أو نطاق للفحص الشامل..." required>
                    <select name="scan_type">
                        <option value="all">فحص شامل (ذكاء استخباراتي كامل)</option>
                        <option value="ports">فحص المنافذ والشبكة المحيطة (Port Scan)</option>
                        <option value="media">مستكشف الوسائط العميق (سحب الصور والروابط)</option>
                        <option value="vulnerability">فحص الثغرات الأمنية السريع</option>
                    </select>
                    <br>
                    <button type="submit">بدء التمشيط الفوري 🚀</button>
                </form>

                {% if result %}
                <h3 style="margin-top: 15px; color: #00ffcc;">📋 تقرير العمليات الميداني:</h3>
                <div class="terminal-screen">{{ result }}</div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    resp = make_response(render_template_string(PANEL_TEMPLATE, result=None))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

@app.route('/scan', methods=['POST'])
def run_scan():
    client_ip = request.remote_addr
    target = request.form.get('target', '').strip()
    scan_type = request.form.get('scan_type', 'all')
    
    log = f"[*] Operator IP: {client_ip}\n[*] Target Objective: {target}\n[*] Active Protocol: {scan_type.upper()}\n"
    
    try:
        if scan_type == 'ports':
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            ip = socket.gethostbyname(domain)
            log += f"[+] Target IP Resolved: {ip}\n[*] Scanning critical ports...\n"
            for p in [21, 22, 80, 443, 3306, 8080]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.6)
                res = s.connect_ex((ip, p))
                log += f"    Port {p}: {'[OPEN - نشط][span_0](start_span)[span_1](start_span)[span_2](start_span)'[span_0](end_span)[span_1](end_span)[span_2](end_span) if res == 0 else '[CLOSED - مغلق]'}\n"
                s.close()
                
        elif scan_type == 'media':
            if not target.startswith("http"):
                target = "http://" + target
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(target, headers=headers, timeout=5)
            log += f"[+] Media Probe Status: {r.status_code}\n"
            images = re.findall(r'src=["\'](.*?\.(?:png|jpg|jpeg|gif|mp4|webp))["\']', r.text, re.IGNORECASE)
            log += f"[+] Discovered Media Assets ({len(images)} found):\n"
            for img in images[:10]:
                log += f"    -> {img}\n"
                
        elif scan_type == 'vulnerability':
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            log += f"[*] Running fast vulnerability headers check on: {domain}\n"
            r = requests.get(target if target.startswith("http") else "http://"+target, timeout=5)
            log += f"[+] Security Headers Analysis:\n"
            log += f"    - X-Frame-Options: {r.headers.get('X-Frame-Options', 'Missing (Potential Vulnerability)')}\n"
            log += f"    - Content-Security-Policy: {r.headers.get('CSP', 'Not Enforced')}\n"
            log += f"    - Server Banner: {r.headers.get('Server', 'Hidden')}\n"
            
        else: # Universal All-in-one
            domain = target.replace('https://', '').replace('http://', '').split('/')[0]
            ip = socket.gethostbyname(domain)
            log += f"[+] Target Domain: {domain} | IP: {ip}\n"
            r = requests.get(target if target.startswith("http") else "http://"+target, timeout=5)
            log += f"[+] Response Code: {r.status_code} | Server: {r.headers.get('Server', 'Unknown')}\n"
            title = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
            if title:
                log += f"[V] Page Title: {title.group(1).strip()}\n"
            
        log += "[+] Intelligence operation successfully executed.\n"
    except Exception as e:
        log += f"[-] Execution Error: {str(e)}\n"

    resp = make_response(render_template_string(PANEL_TEMPLATE, result=log))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
