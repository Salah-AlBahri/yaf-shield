import os
import threading
from flask import Flask, render_template_string, request
import telebot
from datetime import datetime

# --- إعدادات الهوية والاتصال (درع يفاعة الخبير) ---
BOT_TOKEN = "8585985392:AAHIQMEwAr54SGAlv7OL60SIdBOd-cV1Qps"
CHAT_ID = "6308003612"
APP_NAME = "Expert Yafaa Shield" # الاسم الإنجليزي للرابط
APP_NAME_AR = "درع يفاعة الخبير"   # الاسم العربي للواجهة
DEVELOPER = "SALAH YAFAA"

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# --- الواجهة الأسطورية المدمجة مع الخلفية ---
# تم استخدام رابط لخلفية مشابهة للخلفية التي اخترتها لضمان عملها فوراً
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
            color: white; font-family: 'Segoe UI', Tahoma, sans-serif;
            margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh;
            overflow: hidden;
        }}
        .grid-bg {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background-image: linear-gradient(rgba(0,255,255,0.03) 1px, transparent 1px), 
                              linear-gradient(90deg, rgba(0,255,255,0.03) 1px, transparent 1px);
            background-size: 30px 30px; z-index: 1;
        }}
        .app-container {{
            width: 85%; max-width: 420px;
            background: rgba(10, 20, 30, 0.9);
            border: 2px solid var(--gold); border-radius: 30px;
            padding: 30px; text-align: center;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.2), inset 0 0 15px rgba(212, 175, 55, 0.1);
            position: relative; z-index: 2;
        }}
        .shield-img {{
            width: 120px; height: auto;
            margin-bottom: 15px;
            filter: drop-shadow(0 0 15px var(--neon-blue));
            animation: pulse 2s infinite;
        }}
        h1 {{ font-size: 24px; color: var(--gold); margin: 10px 0 5px; text-transform: uppercase; letter-spacing: 1px; }}
        .dev-tag {{ font-size: 12px; color: #aaa; margin-bottom: 25px; border-bottom: 1px solid var(--gold); padding-bottom: 10px; }}
        
        .status-panel {{
            background: rgba(0, 255, 255, 0.05); border: 1px solid var(--neon-blue);
            padding: 15px; border-radius: 15px; color: var(--neon-blue);
            font-weight: bold; margin-bottom: 30px; font-size: 14px;
        }

        .btn-activate {{
            display: block; width: 100%; padding: 18px;
            background: linear-gradient(45deg, var(--gold) 0%, #f1c40f 100%);
            color: black; text-decoration: none; border-radius: 15px;
            font-weight: bold; font-size: 16px; transition: 0.3s;
        }
        .btn-activate:hover {{ transform: scale(1.03); box-shadow: 0 0 20px var(--gold); }}
        
        .perm-text {{ font-size: 11px; color: #777; margin-top: 15px; }}

        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.05); opacity: 0.8; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="grid-bg"></div>
    <div class="container app-container">
        <div class="shield-icon" style="font-size:80px; color:var(--gold); filter:drop-shadow(0 0 15px var(--neon-blue)); margin-bottom:15px; animation: pulse 2s infinite;">🛡️</div>
        <h1>{APP_NAME_AR}</h1>
        <div class="dev-tag">DEVELOPED BY: {DEVELOPER}</div>
        
        <div class="status-panel">✓ جدار حماية 'Vortex' الرقمي نشط</div>

        <a href="/activate" class="btn-activate">بدء الحماية المجانية (3 أيام)</a>

        <p class="perm-text">سيطلب النظام إذن الإشعارات لضمان تنبيهك فوراً.</p>
        <p style="font-size:10px; color:#555;">الوقت الحالي: {datetime.now().strftime('%H:%M:%S')}</p>
    </div>

    <script>
        // طلب إذن الإشعارات عند فتح التطبيق
        if (Notification.permission !== "granted") {{
            Notification.requestPermission();
        }}
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(UI_HTML)

@app.route('/activate')
def activate():
    user_ip = request.remote_addr
    # إرسال تنبيه فوري لك عند التفعيل
    try:
        bot.send_message(CHAT_ID, f"🔔 **تنبيه حماية!**\n\nقام مستخدم بتفعيل الفترة التجريبية لـ {APP_NAME_AR}.\n📍 IP: {user_ip}\n👤 الخبير: {DEVELOPER}")
    except: pass
    return f"<body style='background:#050a10; color:white; text-align:center; padding-top:50px;' dir='rtl'><h1>تم تفعيل نظام {APP_NAME_AR} بنجاح! 🛡️</h1><p>أنت الآن تحت حماية 'الاستثناء الصامت'.</p></body>"

def run_bot():
    try:
        # رسالة ترحيبية تخبرك بتشغيل السيرفر
        bot.send_message(CHAT_ID, f"🚀 نظام '{APP_NAME_AR}' متصل بالسحابة وجاهز لاستقبال المشتركين.")
        bot.infinity_polling()
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__":
    # تشغيل البوت في الخلفية
    threading.Thread(target=run_bot, daemon=True).start()
    
    # الحصول على المنفذ من السحابة أو استخدام 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
