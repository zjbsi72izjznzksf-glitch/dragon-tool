from flask import Flask, render_template_string, request
import hashlib
import base64
import requests
import socket
import ssl
from datetime import datetime
from urllib.parse import urlparse, parse_qs
import math

app = Flask(__name__)

# سجلات التدقيق والأحداث المركزية (SIEM Core)
audit_logs = []

def log_event(event_type, details):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{event_type}] {details}"
    audit_logs.insert(0, log_entry)
    if len(audit_logs) > 35:
        audit_logs.pop()

# HTML Template (Master Suite Edition)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Dragon Station [Master Cyber Defense Suite]</title>
    <style>
        body { background-color: #0b0f19; color: #c9d1d9; font-family: monospace; padding: 20px; }
        h1 { color: #58a6ff; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
        .box { background: #161b22; border: 1px solid #30363d; padding: 15px; margin-bottom: 20px; border-radius: 6px; }
        input[type="text"] { background: #0d1117; border: 1px solid #30363d; color: #c9d1d9; padding: 8px; width: 70%; border-radius: 4px; font-family: monospace; }
        button { background: #238636; color: white; border: none; padding: 8px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #2ea043; }
        .result { margin-top: 10px; padding: 10px; background: #010409; border-left: 4px solid #58a6ff; font-size: 13px; }
        ul { list-style-type: none; padding: 0; }
        li { padding: 4px 0; border-bottom: 1px dashed #30363d; font-size: 12px; }
        pre { white-space: pre-wrap; word-wrap: break-word; color: #3fb950; }
        .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        @media(max-width: 768px) { .grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <h1>🐉 Dragon Station [Master Cyber Defense & Operations Suite]</h1>
    <p>منصة العمليات الأمنية والتدقيق السيبراني المتكاملة (12 وحدة تخصصية شاملة)</p>

    <div class="grid">
        <!-- 1. Password Entropy Auditor -->
        <div class="box">
            <h3>1. مدقق سياسة وقوة كلمات المرور</h3>
            <form method="POST" action="/audit_password">
                <input type="text" name="password" placeholder="أدخل كلمة مرور للاختبار..." required>
                <button type="submit">تقييم 🚀</button>
            </form>
            {% if pwd_result %}
            <div class="result"><strong>النتيجة:</strong> {{ pwd_result }} | <strong>الإنتروبي:</strong> {{ pwd_entropy }} بت</div>
            {% endif %}
        </div>

        <!-- 2. Security Headers Audit -->
        <div class="box">
            <h3>2. فحص رؤوس أمان المواقع</h3>
            <form method="POST" action="/audit_headers">
                <input type="text" name="url" placeholder="example.com" required>
                <button type="submit">فحص 🛡️</button>
            </form>
            {% if header_results %}
            <div class="result">
                <ul>
                {% for header, status in header_results.items() %}
                    <li>{{ header }}: {{ status }}</li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>

        <!-- 3. SSL/TLS Certificate Auditor -->
        <div class="box">
            <h3>3. فحص صلاحية شهادات SSL/TLS</h3>
            <form method="POST" action="/audit_ssl">
                <input type="text" name="ssl_domain" placeholder="example.com" required>
                <button type="submit">فحص 🔒</button>
            </form>
            {% if ssl_result %}
            <div class="result">{{ ssl_result | safe }}</div>
            {% endif %}
        </div>

        <!-- 4. HTTP Methods Auditor -->
        <div class="box">
            <h3>4. فحص طرق اتصال الويب (HTTP Methods)</h3>
            <form method="POST" action="/audit_methods">
                <input type="text" name="methods_url" placeholder="https://example.com" required>
                <button type="submit">فحص 🌐</button>
            </form>
            {% if methods_result %}
            <div class="result"><strong>الطرق:</strong> {{ methods_result }}</div>
            {% endif %}
        </div>

        <!-- 5. Robots.txt Auditor -->
        <div class="box">
            <h3>5. فحص ملف التوجيه والمسارات (Robots.txt)</h3>
            <form method="POST" action="/audit_robots">
                <input type="text" name="robots_domain" placeholder="example.com" required>
                <button type="submit">فحص 📂</button>
            </form>
            {% if robots_result %}
            <div class="result"><pre>{{ robots_result | safe }}</pre></div>
            {% endif %}
        </div>

        <!-- 6. DNS & IP Lookup -->
        <div class="box">
            <h3>6. استعلامات النطاقات وعنوان IP (DNS Lookup)</h3>
            <form method="POST" action="/audit_dns">
                <input type="text" name="dns_domain" placeholder="example.com" required>
                <button type="submit">تحليل 🔍</button>
            </form>
            {% if dns_result %}
            <div class="result">{{ dns_result | safe }}</div>
            {% endif %}
        </div>

        <!-- 7. URL & Parameter AppSec Analyzer -->
        <div class="box">
            <h3>7. محلل هيكل الروابط والمعلمات (AppSec)</h3>
            <form method="POST" action="/audit_url">
                <input type="text" name="target_url" placeholder="https://ex.com/page?id=1&user=admin" required>
                <button type="submit">تفكيك ⚙️</button>
            </form>
            {% if url_result %}
            <div class="result">{{ url_result | safe }}</div>
            {% endif %}
        </div>

        <!-- 8. Port Reachability Recon -->
        <div class="box">
            <h3>8. فحص المنافذ السريع (Port Reconnaissance)</h3>
            <form method="POST" action="/audit_ports">
                <input type="text" name="port_target" placeholder="example.com" required>
                <button type="submit">فحص 🔌</button>
            </form>
            {% if port_result %}
            <div class="result">{{ port_result | safe }}</div>
            {% endif %}
        </div>

        <!-- 9. Cryptographic Hash & Codec -->
        <div class="box">
            <h3>9. حاسبة البصمات والمشفرات (Crypto & Codecs)</h3>
            <form method="POST" action="/audit_crypto">
                <input type="text" name="crypto_text" placeholder="أدخل نصاً للتشفير/البصمة..." required>
                <button type="submit">معالجة 🔐</button>
            </form>
            {% if crypto_result %}
            <div class="result">{{ crypto_result | safe }}</div>
            {% endif %}
        </div>

        <!-- 10. Vulnerability / CVE Mock Database -->
        <div class="box">
            <h3>10. فاحص الثغرات والتوافق (CVE & Software Watch)</h3>
            <form method="POST" action="/audit_cve">
                <input type="text" name="software_name" placeholder="أدخل اسم خدمة (مثل apache, openssl)..." required>
                <button type="submit">مطابقة 📊</button>
            </form>
            {% if cve_result %}
            <div class="result">{{ cve_result | safe }}</div>
            {% endif %}
        </div>
    </div>

    <!-- 11. Network / Local Interface Simulation -->
    <div class="box">
        <h3>11. حالة واجهات الشبكة المحلية (Network Interfaces Diagnostic)</h3>
        <form method="POST" action="/audit_net">
            <button type="submit" style="background:#1f6feb;">فحص حالة الاتصال المحلي 🌐</button>
        </form>
        {% if net_result %}
        <div class="result">{{ net_result | safe }}</div>
        {% endif %}
    </div>

    <!-- 12. SIEM Log Monitor -->
    <div class="box">
        <h3>12. نظام مراقبة ورصد السجلات اللحظية (SIEM Core)</h3>
        <form method="POST" action="/audit_siem">
            <button type="submit" style="background:#da3633;">تحديث وإحصاء السجلات 📊</button>
        </form>
        {% if siem_result %}
        <div class="result">{{ siem_result | safe }}</div>
        {% endif %}
    </div>

    <!-- Audit Logs Trail -->
    <div class="box">
        <h3>📋 سجل الأحداث والعمليات الأمنية (Audit Trail)</h3>
        <ul>
            {% for log in logs %}
            <li>{{ log }}</li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, logs=audit_logs)

@app.route('/audit_password', methods=['POST'])
def audit_password():
    pwd = request.form.get('password', '')
    length = len(pwd)
    charset = sum([26 if c.islower() else 0 for c in pwd]) + \
              sum([26 if c.isupper() else 0 for c in pwd]) + \
              sum([10 if c.isdigit() else 0 for c in pwd]) + \
              sum([32 if not c.isalnum() else 0 for c in pwd])
    entropy = round(length * math.log2(charset if charset > 0 else 1), 2)
    res = "ضعيفة جداً ومكشوفة ⚠️" if entropy < 28 else ("متوسطة الحماية ⚡" if entropy < 50 else "قوية جداً وممتازة 🛡️")
    log_event("Password Audit", "تقييم تعقيد كلمة المرور.")
    return render_template_string(HTML_TEMPLATE, pwd_result=res, pwd_entropy=entropy, logs=audit_logs)

@app.route('/audit_headers', methods=['POST'])
def audit_headers():
    target = request.form.get('url', '').strip()
    if not target.startswith('http'): target = 'https://' + target
    results = {}
    try:
        r = requests.get(target, timeout=5)
        for sh in ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']:
            results[sh] = "مفعل ✅" if sh in r.headers else "مفقود ⚠️"
    except Exception as e:
        results['خطأ'] = str(e)
    log_event("Headers Audit", f"فحص رؤوس: {target}")
    return render_template_string(HTML_TEMPLATE, header_results=results, logs=audit_logs)

@app.route('/audit_ssl', methods=['POST'])
def audit_ssl():
    domain = request.form.get('ssl_domain', '').strip().replace('https://', '').replace('http://', '').split('/')[0]
    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                issuer = dict(x[0] for x in cert['issuer'])
                res_text = f"المصدر: {issuer.get('commonName', 'غير معروف')}<br>الانتهاء: {cert['notAfter']}<br>الحالة: صالحة وموثوقة 🔒"
    except Exception as e:
        res_text = f"فشل الفحص: {e}"
    log_event("SSL Audit", f"شهادة: {domain}")
    return render_template_string(HTML_TEMPLATE, ssl_result=res_text, logs=audit_logs)

@app.route('/audit_methods', methods=['POST'])
def audit_methods():
    target = request.form.get('methods_url', '').strip()
    if not target.startswith('http'): target = 'https://' + target
    try:
        r = requests.options(target, timeout=5)
        methods_str = r.headers.get('Allow', 'غير متوفر في الرؤوس مباشرة (محظور)')
    except Exception as e:
        methods_str = f"خطأ: {e}"
    log_event("HTTP Methods", f"فحص طرق: {target}")
    return render_template_string(HTML_TEMPLATE, methods_result=methods_str, logs=audit_logs)

@app.route('/audit_robots', methods=['POST'])
def audit_robots():
    domain = request.form.get('robots_domain', '').strip().replace('https://', '').replace('http://', '').split('/')[0]
    try:
        r = requests.get(f"https://{domain}/robots.txt", timeout=5)
        res = r.text[:600] if r.status_code == 200 else f"رمز الاستجابة: {r.status_code}"
    except Exception as e:
        res = f"خطأ: {e}"
    log_event("Robots Audit", f"ملف توجيه: {domain}")
    return render_template_string(HTML_TEMPLATE, robots_result=res, logs=audit_logs)

@app.route('/audit_dns', methods=['POST'])
def audit_dns():
    domain = request.form.get('dns_domain', '').strip().replace('https://', '').replace('http://', '').split('/')[0]
    try:
        ip = socket.gethostbyname(domain)
        dns_res = f"النطاق: {domain}<br>عنوان IP: <span style='color:#58a6ff;'>{ip}</span> 🌐"
    except Exception as e:
        dns_res = f"فشل الحل: {e}"
    log_event("DNS Lookup", f"استعلام DNS: {domain}")
    return render_template_string(HTML_TEMPLATE, dns_result=dns_res, logs=audit_logs)

@app.route('/audit_url', methods=['POST'])
def audit_url():
    url = request.form.get('target_url', '').strip()
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    res = f"المضيف: {parsed.hostname}<br>المسار: {parsed.path}<br>المعلمات (Parameters): {params if params else 'لا توجد معلمات'}"
    log_event("URL Parser", f"تحليل رابط: {parsed.hostname}")
    return render_template_string(HTML_TEMPLATE, url_result=res, logs=audit_logs)

@app.route('/audit_ports', methods=['POST'])
def audit_ports():
    target = request.form.get('port_target', '').strip().replace('https://', '').replace('http://', '').split('/')[0]
    ports = [80, 443, 21, 22, 8080]
    status_text = ""
    try:
        ip = socket.gethostbyname(target)
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            res = s.connect_ex((ip, p))
            status_text += f"المنفذ {p}: {'مفتوح ✅' if res == 0 else 'مغلق 🔒'}<br>"
            s.close()
    except Exception as e:
        status_text = f"خطأ: {e}"
    log_event("Port Scanner", f"فحص منافذ: {target}")
    return render_template_string(HTML_TEMPLATE, port_result=status_text, logs=audit_logs)

@app.route('/audit_crypto', methods=['POST'])
def audit_crypto():
    text = request.form.get('crypto_text', '')
    md5_h = hashlib.md5(text.encode()).hexdigest()
    sha256_h = hashlib.sha256(text.encode()).hexdigest()
    b64_enc = base64.b64encode(text.encode()).decode()
    res = f"MD5: {md5_h}<br>SHA256: {sha256_h}<br>Base64: {b64_enc}"
    log_event("Crypto Calculator", "حساب التشفير والبصمات.")
    return render_template_string(HTML_TEMPLATE, crypto_result=res, logs=audit_logs)

@app.route('/audit_cve', methods=['POST'])
def audit_cve():
    sw = request.form.get('software_name', '').strip().lower()
    #قاعدة بيانات مصغرة محاكاة لفحص الثغرات الشهيرة
    cve_db = {
        'openssl': 'تحذير محتمل: تحقق من إصدارات OpenSSL القديمة لتفادي ثغرات Heartbleed أو تجاوز المخازن.',
        'apache': 'ملاحظة أمنية: تأكد من تعطيل عرض محتويات المجلدات (Directory Listing) وإخفاء الإصدار.',
        'nginx': 'ملاحظة أمنية: تأكد من تحديث خادم الويب وتجنب إعدادات التوجيه الخاطئة.',
        'ssh': 'توصية: تأكد من إيقاف تسجيل الدخول الجذري (Root Login) عبر SSH واستخدام المفاتيح حصراً.'
    }
    res = cve_db.get(sw, f"الخدمة '{sw}' ليس لها تحذيرات حرجة مسجلة في قاعدة التقييم السريع المحلية.")
    log_event("CVE Watch", f"فحص توافق ثغرات لـ: {sw}")
    return render_template_string(HTML_TEMPLATE, cve_result=res, logs=audit_logs)

@app.route('/audit_net', methods=['POST'])
def audit_net():
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        res = f"اسم المضيف المحلي: {hostname}<br>عنوان IP المحلي: <span style='color:#58a6ff;'>{local_ip}</span><br>حالة واجهة الشبكة: متصل ونشط 🟢"
    except Exception as e:
        res = f"تعذر استعلام الشبكة المحلية: {e}"
    log_event("Network Diagnostic", "فحص واجهات الشبكة المحلية.")
    return render_template_string(HTML_TEMPLATE, net_result=res, logs=audit_logs)

@app.route('/audit_siem', methods=['POST'])
def audit_siem():
    count = len(audit_logs)
    res = f"إجمالي العمليات المسجلة في ذاكرة SIEM: {count}<br>حالة النظام الأمنية: مراقبة مستمرة ومستقرة 🟢"
    log_event("SIEM Core", "فحص وإحصاء السجلات الأمنية.")
    return render_template_string(HTML_TEMPLATE, siem_result=res, logs=audit_logs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
