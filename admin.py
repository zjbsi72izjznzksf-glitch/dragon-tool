import requests
import time
import sys

# إعدادات الاتصال بالسيرفر السيادي
SERVER_URL = "https://dragon-tool.onrender.com"
SECRET_KEY = "dragon_master_777"

def clear_screen():
    print("\033[H\033[J", end="")

def main_dashboard():
    while True:
        clear_screen()
        print("========================================")
        print("🐉 محطة القيادة والسيطرة - أداة التنين (Live)")
        print("========================================")
        print("[1] سحب سجلات البحث والحركات الحقيقية من السيرفر")
        print("[2] تحديث حالة النظام أو رسالة الترحيب على الموقع")
        print("[3] مراقبة حية تلقائية (تحديث كل 5 ثوانٍ)")
        print("[4] خروج")
        print("========================================")
        
        choice = input("اختر رقم العملية يا زعيم -> ").strip()
        
        if choice == "1":
            fetch_logs()
        elif choice == "2":
            update_server_state()
        elif choice == "3":
            live_monitor()
        elif choice == "4":
            print("إغلاق محطة القيادة... دمتم سالمين 🛡️")
            sys.exit(0)
        else:
            print("[-] خيار غير صحيح، حاول مرة أخرى.")
            time.sleep(1.5)

def fetch_logs():
    print("\n[*] جاري الاتصال بالسيرفر وسحب أحدث السجلات...")
    try:
        # نرسل طلب مع المفتاح السري لجلب البيانات
        response = requests.post(f"{SERVER_URL}/command", json={"secret_key": SECRET_KEY})
        if response.status_code == 200:
            data = response.json()
            print("\n[+] --- سجلات البحث الحقيقية للزوار ---")
            search_history = data.get("search_history", [])
            if search_history:
                for idx, log in enumerate(search_history, 1):
                    print(f"{idx}. {log}")
            else:
                print("لا توجد عمليات بحث مسجلة حتى الآن.")
                
            print("\n[+] --- سجلات التسلل أو الحماية ---")
            intrusion_logs = data.get("logs", [])
            if intrusion_logs:
                for log in intrusion_logs:
                    print(f" - {log}")
            else:
                print("الموقع آمن تماماً، لا محاولات اختراق.")
        else:
            print("[-] خطأ في المصادقة أو السيرفر لا يزال يستجيب.")
    except Exception as e:
        print(f"[-] حدث خطأ في الاتصال بالشبكة: {e}")
        
    input("\nاضغط Enter للعودة للقائمة الرئيسية...")

def update_server_state():
    print("\n--- تحديث محتوى الموقع عن بُعد ---")
    new_welcome = input("أدخل رسالة الترحيب الجديدة (أو اضغط Enter لتخطيها): ").strip()
    new_status = input("أدخل حالة النظام الجديدة (أو اضغط Enter لتخطيها): ").strip()
    
    payload = {"secret_key": SECRET_KEY}
    if new_welcome: payload["welcome"] = new_welcome
    if new_status: payload["status"] = new_status
    
    try:
        response = requests.post(f"{SERVER_URL}/command", json=payload)
        if response.status_code == 200:
            print("[+] تم تحديث السيرفر بنجاح على الهواء مباشرة! 🚀")
        else:
            print("[-] فشل التحديث، تأكد من المفتاح السري.")
    except Exception as e:
        print(f"[-] خطأ في الاتصال: {e}")
        
    input("\nاضغط Enter للعودة...")

def live_monitor():
    print("\n[i] بدء وضع المراقبة الحية (اضغط Ctrl+C للإيقاف)...")
    try:
        while True:
            response = requests.post(f"{SERVER_URL}/command", json={"secret_key": SECRET_KEY})
            if response.status_code == 200:
                data = response.json()
                search_history = data.get("search_history", [])
                clear_screen()
                print("=== [ Live Monitor Mode - Dragon Tool ] ===")
                print(f"آخر تحديث: {time.strftime('%H:%M:%S')}")
                print(f"عدد عمليات الاستعلام الحقيقية المسجلة: {len(search_history)}")
                if search_history:
                    print("\nأحدث عملية مسجلة:")
                    print(search_history[-1])
                print("\n[اضغط Ctrl+C للرجوع]")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[!] تم إيقاف وضع المراقبة الحية.")
        time.sleep(1)

if __name__ == "__main__":
    main_dashboard()
