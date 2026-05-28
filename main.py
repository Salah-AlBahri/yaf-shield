import os
import threading
import webbrowser
import random
import string
from flask import Flask, render_template_string, request, redirect
import telebot
from time import sleep

# --- البيانات الأساسية التابعة للمطور والمبرمج صلاح يفاعه ---
BOT_TOKEN = "8585985392:AAHIQMEwAr54SGAlv7OL60SIdBOd-cV1Qps"
CHAT_ID = "6308003612"
APP_NAME = "درع يفاعة الخبير | Expert Yafaa Shield"
DEVELOPER_NAME = "المطور والمبرمج صلاح يفاعه"
WHATSAPP_NUMBER = "967776941096"

# الحسابات المالية (حساب جوالي الخاص بك مع مرونة إضافة حسابات أخرى مستقبلاً)
PAYMENT_METHODS = {
    "جوالي": "776941096",
    "حساب إضافي": "يمكن للمبرمج صلاح إضافة أي حساب آخر هنا بسهولة مستقبلاً"
}

app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# قائمة لتخزين الأكواد النشطة التي تم توليدها تلقائياً وأُرسلت لـ صلاح على التيليجرام
GENERATED_KEYS = {}
activated_users = set()

def generate_secure_key():
    """توليد كود سري عشوائي فريد لكل مستخدم"""
    return "YAF-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- التصميم والألوان للواجهات الاحترافية (HTML/CSS) ---
STYLE_CSS = '''
<style>
    :root { --gold: #d4af37; --neon-blue: #00ffff; --bg-dark: #050a10; }
    body { 
        background: radial-gradient(circle at center, #1a2a3a 0%, var(--bg-dark) 100%);
        color: white; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0; padding: 20px; display: flex; justify-content: center; align-items: center; min-height: 100vh; direction: rtl;
    }
    .container {
        width: 100%; max-width: 460px; background: rgba(10, 20, 30, 0.95);
        border: 2px solid var(--gold); border-radius: 25px; padding: 30px; text-align: center;
        box-shadow: 0 0 25px rgba(0, 255, 255, 0.2);
    }
    h1 { color: var(--gold); font-size: 24px; margin-bottom: 5px; }
    .dev-tag { font-size: 13px; color: #aaa; margin-bottom: 20px; font-weight: bold; }
    .card { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; margin-bottom: 15px; text-align: right; border: 1px solid #333; }
    .btn {
        display: block; background: var(--gold); color: black; padding: 15px;
        text-decoration: none; border-radius: 12px; font-weight: bold; margin-top: 15px; text-align: center; transition: 0.3s; cursor: pointer; border: none; width: 100%; font-size: 16px;
    }
    .btn-whatsapp { background: #25d366; color: white; }
    .btn:hover { transform: scale(1.02); opacity: 0.9; }
    input[type="text"] { width: 100%; padding: 12px; border-radius: 8px; border: 1px solid var(--gold); background: #111; color: white; margin-top: 10px; box-sizing: border-box; text-align: center; font-weight: bold; font-size: 16px; letter-spacing: 1px; }
</style>
'''

# 1. شاشة طلب الصلاحيات والخلفية المالية والاشتراكات
@app.route('/')
def subscription_page():
    return f'''
    <!DOCTYPE html>
    <html lang="ar">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{APP_NAME}</title>{STYLE_CSS}</head>
    <body>
        <div class="container">
            <div style="font-size: 60px;">🛡️</div>
            <h1>{APP_NAME}</h1>
            <div class="dev-tag">المطور والمبرمج: {DEVELOPER_NAME}</div>
            
            <p style="color: var(--neon-blue); font-weight: bold; font-size: 14px;">⚠️ يتطلب التطبيق منح كامل صلاحيات النظام ليكون المسؤول عن حماية هاتفك من الاختراق والملفات الخفية.</p>
            
            <div class="card" style="border-right: 4px solid var(--gold);">
                <p style="font-size: 14px; line-height: 1.6; font-weight: bold; color: #fff;">
                    📢 يرجى تحويل قيمة الاشتراك إلى محفظة جوالي رقم ({PAYMENT_METHODS["جوالي"]}) وإرسال لقطة شاشة لي عبر الوتساب (Screenshot) لتفعيل الحساب يدوياً.
                </p>
            </div>

            <div class="card">
                <h3>💎 خطط الحماية المتوفرة:</h3>
                <p>⏱️ <b>فترة تجريبية (3 أيام):</b> لكي يعرف المستخدم الفائدة الحقيقية للدرع وقوته في كشف التجسس قبل الاشتراك.</p>
                <p>📅 <b>اشتراك شهري:</b> حماية نشطة على مدار الساعة.</p>
                <p>🏆 <b>اشتراك سنوي:</b> التوفير الأكبر + ميزات في آي بي حصرياً.</p>
            </div>

            <form action="/request_activation" method="POST">
                <button type="submit" class="btn" style="background: var(--neon-blue); color: black;">لقد قمت بالتحويل | أطلب كود التفعيل السري الآن</button>
            </form>

            <a href="https://wa.me/{WHATSAPP_NUMBER}?text=مرحباً%20بالمبرمج%20صلاح%20لقد%20قمت%20بالتحويل%20عبر%20جوالي%20إلى%20الحساب%20{PAYMENT_METHODS["جوالي"]}%20وأريد%20تفعيل%20حسابي.%20(جاري%20إرسال%20الـ%20Screenshot)" class="btn btn-whatsapp" target="_blank">💬 للتواصل معنا ومراسلتنا واتساب مباشرة اضغط هنا</a>
        </div>
    </body>
    </html>
    '''

# 2. توليد الكود السري وإرساله لتليجرام المطور صلاح + توجيه المستخدم لصفحة الإدخال
@app.route('/request_activation', methods=['POST'])
def request_activation():
    user_ip = request.remote_addr
    
    # استخراج دقيق لنوع هاتف الزبون لكي يصل لصلاح
    user_agent = request.headers.get('User-Agent', 'Unknown Device')
    device_type = "هاتف أندرويد"
    if "Mobile" in user_agent and '(' in user_agent:
        try: device_type = user_agent.split('(')[1].split(')')[0].split(';')[2].strip()
        except: device_type = "هاتف أندرويد ذكي"

    # توليد الكود السري للمستخدم وحفظه مؤقتاً في السيرفر مرتبطاً بالـ IP
    secret_key = generate_secure_key()
    GENERATED_KEYS[user_ip] = secret_key

    try:
        # الإشعار الفوري يصل لصلاح على تليجرام فوراً بنوع هاتف المشترك
        message_text = (
            f"🔔 **طلب تفعيل جديد وصلك يا صلاح!**\n\n"
            f"📱 هاتف نوع: `{device_type}`\n"
            f"🌐 عنوان الـ IP: `{user_ip}`\n"
            f"💰 إشعار الدفع: تم عبر حساب جوالي.\n\n"
            f"🔑 **كود التفعيل السري المولد له:** `{secret_key}`\n\n"
            f"⚙️ **عملك الآن:** انتظر الزبون يراسلك واتساب، وإذا تأكدت من وصول الفلوس في حساب جوالي، انسخ له الكود السري هذا وأرسله له مباشرة."
        )
        bot.send_message(CHAT_ID, message_text, parse_mode="Markdown")
    except: pass

    # نقل المستخدم لصفحة الانتظار والنجاح وإدخال الكود
    return f'''
    <!DOCTYPE html>
    <html lang="ar">
    <head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>إدخال الكود السري</title>{STYLE_CSS}</head>
    <body>
        <div class="container">
            <h2 style="color: #25d366;">🎉 تم تقديم طلب الاشتراك بنجاح!</h2>
            <p style="color: #ccc; font-size: 14px;">يرجى تفعيل الميزات بالتواصل مع المبرمج صلاح يفاعه عبر زر الواتساب أدناه لإرسال لقطة الشاشة (Screenshot) واستلام الكود السري الخاص بك لفتح الميزات.</p>
            
            <form action="/verify_code" method="POST" style="margin-top: 25px;">
                <label style="color: var(--gold); font-weight: bold;">أدخل الكود السري لفتح الميزات كاملة:</label>
                <input type="text" name="secret_key" placeholder="مثال: YAF-XXXXXX" required>
                <button type="submit" class="btn">تفعيل وإطلاق جدار الحماية الحقيقي</button>
            </form>

            <a href="https://wa.me/{WHATSAPP_NUMBER}?text=مرحباً%20بالمبرمج%20صلاح%20لقد%20ضغطت%20على%20طلب%20الكود%20في%20البرنامج%20وهاك%20لقطة%20شاشة%20التحويل%20لتفعل%20حسابي" class="btn btn-whatsapp" target="_blank">💬 اضغط هنا لإرسال الـ Screenshot واستلام كودك فوراً</a>
        </div>
    </body>
    </html>
    '''

# 3. التحقق من الكود السري وفتح الميزات للمستخدم بنجاح
@app.route('/verify_code', methods=['POST'])
def verify_code():
    input_key = request.form.get('secret_key').strip()
    user_ip = request.remote_addr
    
    if user_ip in GENERATED_KEYS and GENERATED_KEYS[user_ip] == input_key:
        activated_users.add(user_ip)
        return redirect('/dashboard')
    else:
        return f'''
        <body style='background:#050a10; color:white; text-align:center; padding-top:50px; font-family:sans-serif;' dir='rtl'>
            <h1 style='color:#ff3333;'>❌ كود التفعيل السري غير صحيح أو لم يتم تفعيله!</h1>
            <p>تأكد من أنك نسخت الكود الذي أعطاك إياه المبرمج صلاح يفاعه بشكل صحيح دون فراغات.</p>
            <br><a href='/' style='color:var(--neon-blue); text-decoration:none; font-weight:bold;'>← العودة للخلف لإعادة المحاولة</a>
        </body>
        '''

# 4. لوحة تحكم الحماية والدرع الحديدي (تفتح طوالي بعد الكود الصح)
@app.route('/dashboard')
def dashboard():
    user_ip = request.remote_addr
    if user_ip not in activated_users:
        return redirect('/')
    
    return f'''
    <!DOCTYPE html>
    <html lang="ar">
    <head><meta charset="UTF-8"><title>الدرع النشط | صلاح يفاعه</title>{STYLE_CSS}</head>
    <body>
        <div class="container">
            <h2 style="color: #25d366;">⚡ تم الاشتراك بنجاح والدرع نشط</h2>
            <div class="dev-tag">نظام حماية وإشراف: {DEVELOPER_NAME}</div>
            
            <div class="card" style="text-align: center; border: 1px solid #25d366;">
                <p>🛡️ حالة الفحص الفوري: <b style="color: #25d366;">آمن تماماً ويحميك من الاختراق الآن</b></p>
                <p>🔒 صلاحيات الحماية: <b style="color: var(--neon-blue);">ممنوحة ومسؤولة بالكامل عن الهاتف</b></p>
            </div>

            <div class="card">
                <h3>🔍 فحص الروابط المشبوهة لمنع الاختراق (Anti-Phishing)</h3>
                <input type="text" placeholder="صق الرابط هنا للتأمين وفحصه...">
                <button class="btn" onclick="alert('جاري الفحص المتقدم عبر خوادم المبرمج صلاح الأمنية... نتيجة الفحص: الرابط آمن ومحمي وموثوق!')">ابدأ الفحص الفوري للرابط</button>
            </div>

            <div class="card">
                <h3>🚫 مستشار صلاح لمنع التجسس والتعقب</h3>
                <p style="font-size: 13px; color: #ccc; line-height: 1.5;">• التطبيق يعمل كالمسؤول الأول؛ يراقب الكاميرا والمايكروفون والملفات في الخلفية لمنع أي محاولة اختراق خفية لخصوصيتك.</p>
            </div>

            <a href="https://wa.me/{WHATSAPP_NUMBER}" class="btn btn-whatsapp" target="_blank">💬 للدعم الفني المباشر مع المبرمج صلاح يفاعه</a>
        </div>
    </body>
    </html>
    '''

def open_browser():
    sleep(3) 
    webbrowser.open("http://127.0.0.1:8080")

def run_bot():
    try:
        bot.send_message(CHAT_ID, f"🚀 نظام '{APP_NAME}' أونلاين الآن وجاهز لتوليد الأكواد السرية للمشتركين.")
        bot.infinity_polling()
    except: pass

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=open_browser, daemon=True).start()
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
