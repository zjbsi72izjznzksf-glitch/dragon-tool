from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import datetime
import socket
import urllib.parse
import requests
import re

app = Flask(__name__)
app.secret_key = "dragon_master_absolute_iron_security_999"

site_state = {
    "welcome_message": "سيرفر أبو خالد الحصين - أداة التنين 🐉🛡️",
    "status": "الوضع السيادي الحديدي نشط وآمن ✅",
    "search_logs": []
}

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>سيرفر أبو خالد - التحقق الصارم الحصري</title>
    <style>
        body { background-color: #020202; color: #00ffcc; font-family: Tahoma, sans-serif; text-align: center; padding: 20px; }
        .box { background: #080808; border: 3px solid #ff3333; border-radius: 15px; padding: 30px; max-width: 500px; margin: 40px auto; box-shadow: 0 0 35px rgba(255,51,51,0.3); }
        h1 { color: #ff3333; font-size: 21px; text-shadow: 0 0 10px rgba(255,51,51,0.5); }
        p { color: #ccc; font-size: 13px; line-height: 1.6; text-align: right; }
        input[type="text"] { width: 90%; padding: 11px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; margin: 10px 0; text-align: right; direction: ltr; }
        .name-input { direction: rtl !important; }
        button { padding: 12px 25px; background: #ff3333; color: #fff; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 15px; font-size: 14px; }
        button:hover { background: #cc0000; }
        .warning { background: #1a0000; border: 1px dashed #ff3333; padding: 12px; border-radius: 5px; margin-bottom: 15px; text-align: right; }
        .error-msg { background: #330000; color: #ff6666; border: 1px solid #ff3333; padding: 10px; border-radius: 5px; font-size: 12px; margin-top: 15px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🔒 بوابة الحماية الصارمة (بريد حقيقي حصراً)</h1>
        <div class="warning">
            <p style="color: #ff9999; font-size: 12px; margin:0; text-align: right;">
                تنبيه أمني حديدي: يمنع منعاً باتاً استخدام البريد الوهمي. يجب إدخال بريد جوجل حقيقي (مثال: `yourname@gmail.com`). أي محاولة تلاعب سترفض فوراً.
            </p>
        </div>
        <form method="POST">
            <input type="text" name="username" class="name-input" placeholder="الاسم الحركي للمشغل..." required>
            <input type="text" name="email" placeholder="البريد الحقيقي (name@gmail.com)..." required>
            <button type="submit">التحقق والدخول الميداني 🚀</button>
        </form>
        {% if error %}
        <div class="error-msg">{{ error }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>سيرفر أبو خالد - محطة الاستخبارات الشاملة</title>
    <style>
        body { background-color: #030303; color: #00ffcc; font-family: Tahoma, sans-serif; text-align: center; padding: 10px; margin: 0; }
        .container { display: flex; justify-content: center; align-items: center; min-height: 95vh; }
        .dragon-box { background: #0a0a0a; border: 3px solid #00ffcc; border-radius: 20px; padding: 20px; box-shadow: 0 0 40px rgba(0,255,204,0.3); max-width: 900px; width: 100%; }
        h1 { color: #00ffcc; text-shadow: 0 0 10px #00ffcc; font-size: 20px; margin-bottom: 5px; }
        .subtitle { color: #888; font-size: 12px; margin-bottom: 15px; }
        .panel { background: #111; border: 2px solid #222; padding: 15px; border-radius: 10px; text-align: right; direction: rtl; margin-top: 10px; }
        .panel h3 { color: #ffaa00; margin-top: 0; font-size: 14px; }
        input[type="text"] { width: 63%; padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; text-align: left; direction: ltr; display: inline-block; }
        select { padding: 10px; background: #000; border: 1px solid #00ffcc; color: #00ffcc; border-radius: 5px; font-size: 13px; margin-left: 5px; }
        button { padding: 10px 18px; background: #00ffcc; color: #000; border: none; border-radius: 5px; font-weight: bold; cursor: pointer; margin-top: 10px; }
        button:hover { background: #00b388; }
        .terminal-screen { background: #000; color: #00ff00; border: 1px solid #00ff00; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 11px; text-align: left; direction: ltr; margin-top: 10px; max-height: 260px; overflow-y: auto; white-space: pre-wrap; }
        .user-tag { background: #1a1a1a; border: 1px solid #ffaa00; padding: 5px 10px; border-radius: 5px; font-size: 12px; color: #ffaa00; display: inline-block; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="dragon-box">
            <h1>🐉 سيرفر أبو خالد للاستخبارات الشاملة (محمي حصرياً)</h1>
            <p class="subtitle">فحص وتحليل أي شيء في العالم بمشغلين موثقين بريدياً</p>
            
            <div class="panel">
                <div class="user-tag">👤 المشغل الموثق: {{ user_email }} | الآيبي: {{ client_ip }}</div>
                <h3>🔍 محرك البحث الشامل (كل شيء في العالم):</h3>
                <form method="POST" action="/search" style="text-align: center;">
                    <input type="text" name="target" placeholder="أدخل أي رابط في العالم، موقع، أو هدف للبحث..." required>
                    <select name="scan_type">
                        <option value="universal">تحليل شامل وعام (أي شيء في العالم)</option>
                        <option value="dns">استعلام سجلات الـ DNS العميقة</option>
                        <option value="ports">فحص المنافذ والحالة الشبكية</option>
                    </select>
                    <br>
                    <button type="submit">تنفيذ الفحص الاستخباراتي 🚀</button>
                </form>

                {% if search_result %}
                <h3 style="margin-top: 15px; color: #00ffcc;">📋 تقرير الاستخبارات الميداني:</h3>
                <div class="terminal-screen">{{ search_result }}</div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email').strip().lower()
        
        # فحص سيرفر صارم جداً يرفض أي بريد لا ينتهي حصراً بـ gmail.com أو نطاقات موثقة كبرى
        valid_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com", "proton.me"]
        
        if '@' not in email:
            error = "❌ خطأ أمني: صيغة البريد الإلكتروني غير صحيحة. يجب أن يحتوي على @."
            return render_template_string(LOGIN_TEMPLATE, error=error)
            
        domain_part = email.split('@')[-1]
        local_part = email.split('@')[0]
        
        if domain_part not in valid_domains or len(local_part) < 3:
            error = "❌ تم رفض البريد! يُشترط إدخال بريد حقيقي مسجل (مثل gmail.com) وباسم مستخدم صالح ولا يُقبل البريد الوهمي نهائياً."
            return render_template_string(LOGIN_TEMPLATE, error=error)
            
        session['username'] = username
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template_string(LOGIN_TEMPLATE, error=error)

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template_string(
        DASHBOARD_TEMPLATE, 
        user_email=session['email'],
        client_ip=request.remote_addr,
        search_result=None
    )

@app.route('/search', methods=['POST'])
def real_search():
    if 'email' not in session:
        return redirect(url_for('login'))
        
    client_ip = request.remote_addr
    user_email = session['email']
    target_input = request.form.get('target', '').strip()
    scan_type = request.form.get('scan_type', 'universal')
    
    result_log = f"[*] Verified Operator: {user_email} | IP: {client_ip}\n[*] Objective: {target_input}\n[*] Mode: {scan_type.upper()}\n"
    
    try:
        if scan_type == 'universal':
            if target_input.startswith("http://") or target_input.startswith("https://"):
                parsed_url = urllib.parse.urlparse(target_input)
                domain = parsed_url.netloc
                path = parsed_url.path
                result_log += f"[+] Target URL Domain: {domain}\n"
                result_log += f"[+] Target Path: {path if path else '/'}\n"
                
                try:
                    ip_addr = socket.gethostbyname(domain)
                    result_log += f"[+] Resolved Server IP: {ip_addr}\n"
                except Exception:
                    result_log += f"[-] DNS Warning: Could not resolve IP for {domain}\n"
                
                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    resp = requests.get(target_input, headers=headers, timeout=6, allow_redirects=True)
                    result_log += f"[+] HTTP Code: {resp.status_code}\n"
                    result_log += f"[+] Content-Type: {resp.headers.get('Content-Type', 'Unknown')}\n"
                    result_log += f"[+] Server Signature: {resp.headers.get('Server', 'Hidden')}\n"
                    
                    if "text/html" in resp.headers.get('Content-Type', ''):
                        title_match = re.search(r'<title>(.*?)</title>', resp.text, re.IGNORECASE)
                        if title_match:
                            result_log += f"[V] Target Title: {title_match.group(1).strip()}\n"
                except Exception as ex:
                    result_log += f"[-] Probe Exception: {str(ex)}\n"
            else:
                domain = target_input.split('/')[0]
                ip_addr = socket.gethostbyname(domain)
                result_log += f"[+] Direct Target: {domain}\n"
                result_log += f"[+] Resolved IP: {ip_addr}\n"
                
        elif scan_type == 'dns':
            domain = target_input.replace('https://', '').replace('http://', '').split('/')[0]
            ip_addr = socket.gethostbyname(domain)
            result_log += f"[+] Target Domain: {domain} -> IP: {ip_addr}\n"
            try:
                host_info = socket.gethostbyaddr(ip_addr)
                result_log += f"[+] PTR Hostname: {host_info[0]}\n"
            except:
                result_log += "[-] PTR Record: None found.\n"
                
        elif scan_type == 'ports':
            domain = target_input.replace('https://', '').replace('http://', '').split('/')[0]
            target_ip = socket.gethostbyname(domain)
            result_log += f"[*] Scanning ports on target IP: {target_ip}...\n"
            for p in [80, 443, 21, 22, 8080, 3306]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.7)
                res = s.connect_ex((target_ip, p))
                result_log += f"    Port {p}: {'[OPEN]' if res == 0 else '[CLOSED]'}\n"
                s.close()
                
        result_log += "[+] Intelligence scan successfully completed.\n"
    except Exception as e:
        result_log += f"[-] Scan Error: {str(e)}\n"

    return render_template_string(
        DASHBOARD_TEMPLATE, 
        user_email=session['email'],
        client_ip=client_ip,
        search_result=result_log
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
