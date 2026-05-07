import os
import threading
import webbrowser
from flask import Flask, render_template_string, request
import telebot
from datetime import datetime
from time import sleep

# --- إعدادات الهوية والاتصال (درع يفاعة الخبير) ---
BOT_TOKEN = "8585985392:AAHIQMEwAr54SGAlv7OL60SIdBOd-cV1Qps"
CHAT_ID = "6308003612"
APP_NAME_AR = "درع يفاعة الخبير"
DEVELOPER = "SALAH YAFAA"

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# --- الواجهة الأسطورية المدمجة ---
UI_HTML = f'''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{APP_NAME_AR}</title>
    <style>
        :root {{ --gold: #d4af37; --neon-blue: #00ffff; --bg-dark: #050a10; }}
        body {{ 
            background: radial-gradient(circle at center, #1a2a3a 0%, var(--bg-dark) 100%);
            color: white; font-family: sans-serif;
            margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh;
        }}
        .app-container {{
            width: 85%; max-width: 400px; background: rgba(10, 20, 30, 0.95);
            border: 2px solid var(--gold); border-radius: 25px; padding: 25px; text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }}
        .shield-icon {{ font-size: 70px; margin-bottom: 10px; }}
        h1 {{ color: var(--gold); font-size: 22px; margin: 10px 0; }}
        .dev-tag {{ font-size: 12px; color: #888; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 20px; }}
        .status {{ color: var(--neon-blue); background: rgba(0,255,255,0.1); padding: 10px; border-radius: 10px; font-size: 14px; margin-bottom: 20px; }}
        .btn {{
            display: block; background: var(--gold); color: black; padding: 15px;
            text-decoration: none; border-radius: 12px; font-weight: bold; transition: 0.3s;
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="shield-icon">🛡️</div>
        <h1>{APP_NAME_AR}</h1>
        <div class="dev-tag">DEVELOPED BY: {DEVELOPER}</div>
        <div class="status">✓ نظام الحماية النشط متصل بالخادم</div>
        <a href="/activate" class="btn">تفعيل حماية 72 ساعة مجاناً</a>
        <p style="font-size:10px; color:#444; margin-top:15px;">تاريخ التحديث: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(UI_HTML)

@app.route('/activate')
def activate():
    user_ip = request.remote_addr
    try:
        bot.send_message(CHAT_ID, f"🔔 **تنبيه جديد!**\n\nتم الضغط على تفعيل الحماية\n📍 IP: {user_ip}\n👤 المطور: {DEVELOPER}")
    except: pass
    return f"<body style='background:#050a10; color:white; text-align:center; padding-top:50px;' dir='rtl'><h1>تم طلب التفعيل بنجاح! 🛡️</h1><p>سيصلك إشعار التأكيد قريباً.</p></body>"

def open_browser():
    """وظيفة لفتح الواجهة تلقائياً عند بدء التطبيق"""
    sleep(3) # الانتظار قليلاً لضمان تشغيل السيرفر
    webbrowser.open("http://127.0.0.1:8080")

def run_bot():
    try:
        bot.send_message(CHAT_ID, f"🚀 نظام '{APP_NAME_AR}' بدأ العمل الآن على الأندرويد.")
        bot.infinity_polling()
    except: pass

if __name__ == "__main__":
    # تشغيل البوت وفتح المتصفح في خيوط منفصلة
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    
    # تشغيل سيرفر الويب
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
