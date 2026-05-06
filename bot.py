import logging
import os
import asyncio
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8585985392:AAHIQMEwAr54SGAlv7OL60SIdBOd-cV1Qps"
LOG_FILE = "salah_logs.txt"

async def monitor_logs(context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    last_size = os.path.getsize(LOG_FILE)
    chat_id = context.job.chat_id
    while True:
        await asyncio.sleep(5)
        current_size = os.path.getsize(LOG_FILE)
        if current_size > last_size:
            with open(LOG_FILE, "r") as f:
                f.seek(last_size)
                new_data = f.read()
            if new_data.strip():
                await context.bot.send_message(chat_id=chat_id, text=f"⚠️ تنبيه نشاط جديد:\n\n{new_data}")
            last_size = current_size

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.job_queue.run_once(monitor_logs, 1, chat_id=update.effective_chat.id)
    buttons = [['📜 عرض السجلات', '📊 حالة النظام'], ['🚀 تحديث GitHub']]
    await update.message.reply_text(
        "نظام Silent Manager المطور جاهز يا صلاح 🛡️\nتم تفعيل المراقبة السحابية.",
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == '📜 عرض السجلات':
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = f.read()[-500:]
            await update.message.reply_text(f"آخر السجلات:\n\n{data if data else 'السجلات فارغة.'}")
    elif text == '📊 حالة النظام':
        await update.message.reply_text("النظام مستقر ✅\nالمراقبة: نشطة 🟢\nالموقع: Dhamar, Yemen")
    elif text == '🚀 تحديث GitHub':
        await update.message.reply_text("جاري رفع التحديثات للسحابة... ⏳")
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Auto-update via Bot"], check=True)
            subprocess.run(["git", "push"], check=True)
            await update.message.reply_text("✅ تم تحديث مستودع GitHub بنجاح!")
        except Exception as e:
            await update.message.reply_text(f"❌ فشل التحديث: تأكد من إعدادات الـ Token والإنترنت.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))
    print("البوت السحابي يعمل الآن...")
    app.run_polling()

if __name__ == '__main__':
    main()

