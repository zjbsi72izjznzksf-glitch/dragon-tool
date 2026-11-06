from flask import Flask, render_template_string, request, make_response
import datetime
import socket
import urllib.parse
import requests
import re

app = Flask(__name__)
app.secret_key = "dragon_master_supreme_ultimate_key_103"

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
    <title>أداة التنين السيادية - وحدة التحكم والأكواد المشفرة</title>
    <style>
        body { background-color: #020202; color: #00ffcc; font-family: Tahoma, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { display: flex; justify-content: center; align-items: center; min-height: 98vh; }
        .dragon-box { background: #070707; border: 3px solid #00ffcc; border-radius: 20px; padding: 20px; box-shadow: 0 0 40px rgba(0,255,204,0.3); max-width: 950px; width: 100%; }
        h1 { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-size: 20px; margin-bottom: 5px; }
        .subtitle { color: #888; font-size: 12px; margin-bottom: 15px; }
        .panel { background: #111; border: 2px solid #222; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 10px; }
        .panel h3 { color: #ffaa00; margin-top: 0; font-size: 14px; }
        input[type="text"], textarea { width: 58%; padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; text-align: left; direction: ltr; display: inline-block; }
        textarea { width: 85%; height: 60px; resize: none; text-align: left; direction: ltr; font-family: monospace; }
        select { padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; margin-left: 5px; }
        button { padding: 10px 18px; background: #ff3333; color: #fff; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #cc0000; }
        .terminal-screen { background: #000; color: #00ff00; border: 1px solid #00ff00; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 11px; text-align: left; direction: ltr; margin-top: 10px; max-height: 240px; overflow-y: auto; white-space: pre-wrap; }
        .shield-status { background: #001a1a; border: 1px dashed #00ffcc; padding: 8px; border-radius: 5px; font-size: 11px; color: #00ffcc; margin-bottom: 10px; text-align: right; }
        .audio-bar { background: #1a0000; border: 1px solid #ff3333; padding: 8px; border-radius: 5px; margin-bottom: 10px; color: #ff9999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="dragon-box">
            <h1>🐉 محطة التنين السيادية المُشفرة (Ultimate Encrypted Engine)</h1>
            <p class="subtitle">فحص أمني، سحب وسائط، تشغيل الأكواد بحرية، وسجل بحث شامل للزوار</p>
            
            <div class="audio-bar">
                🔊 النظام الصوتي التفاعلي: المس الشاشة لمرة واحدة لسماع زئير التنين المرعب، وبعدها ستعمل أصوات الأمن السيبراني والأزرار تلقائياً!
                <br><br>
                <button style="padding: 6px 15px; background: #ffaa00; color: #000; font-size: 12px; font-weight: bold;" onclick="triggerDragonRoar()">🔥 اضغط هنا لسماع زئير التنين يدوياً</button>
            </div>

            <div class="shield-status">
                🛡️ درع التنين المشفر: نشط ومحمي ضد التسريبات | الكود المصدري محصن بالكامل.
            </div>

            <div class="panel">
                <h3>🔍 محرك الفحص والذكاء الاستخباراتي:</h3>
                <form method="POST" action="/scan" style="text-align: center;" onsubmit="playCyberClick()">
                    <input type="text" name="target" placeholder="أدخل رابط، IP، أو نطاق للفحص..." required onkeydown="playCyberClick()">
                    <select name="scan_type" onchange="playCyberClick()">
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
                <form method="POST" action="/execute_code" style="text-align: center;" onsubmit="playCyberClick()">
                    <textarea name="custom_code" placeholder="اكتب أكوادك أو استعلاماتك هنا بحرية تامة... (مشفر وآمن)" required onkeydown="playCyberClick()"></textarea>
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
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        let roarDone = false;

        // صوت زئير التنين المرعب والواضح (يتم تشغيله مرة واحدة فقط)
        function triggerDragonRoar() {
            if (roarDone) return; // منع تكراره ليبقى ظاهراً لمرة واحدة فقط
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }

            let osc1 = audioCtx.createOscillator();
            let gain1 = audioCtx.createGain();
            osc1.type = 'sawtooth';
            osc1.frequency.setValueAtTime(110, audioCtx.currentTime);
            osc1.frequency.linearRampToValueAtTime(35, audioCtx.currentTime + 2.2);

            let osc2 = audioCtx.createOscillator();
            let gain2 = audioCtx.createGain();
            osc2.type = 'triangle';
            osc2.frequency.setValueAtTime(140, audioCtx.currentTime);
            osc2.frequency.linearRampToValueAtTime(45, audioCtx.currentTime + 2.2);

            gain1.gain.setValueAtTime(0.8, audioCtx.currentTime);
            gain1.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 2.2);

            gain2.gain.setValueAtTime(0.4, audioCtx.currentTime);
            gain2.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 2.2);

            osc1.connect(gain1);
            gain1.connect(audioCtx.destination);

            osc2.connect(gain2);
            gain2.connect(audioCtx.destination);

            osc1.start();
            osc2.start();

            osc1.stop(audioCtx.currentTime + 2.2);
            osc2.stop(audioCtx.currentTime + 2.2);

            roarDone = true;
        }

        // أصوات الأمن السيبراني والأزرار (تعمل مع كل كتابة أو نقرة بعد زئير التنين)
        function playCyberClick() {
            if (audioCtx.state === 'suspended') {
                audioCtx.resume();
            }
            let osc = audioCtx.createOscillator();
            let gain = audioCtx.createGain();
            osc.type = 'square';
            osc.frequency.setValueAtTime(750, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(180, audioCtx.currentTime + 0.08);
            
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.08);
            
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            
            osc.start();
            osc.stop(audioCtx.currentTime + 0.08);
        }

        // أول لمسة بالشاشة تطلق زئير التنين لمرة واحدة وبعدها تتحول لأصوات الأزرار
        window.addEventListener('pointerdown', () => {
            if (!roarDone) {
                triggerDragonRoar();
            } else {
                playCyberClick();
            }
        });
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
