from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from TikTokApi import TikTokApi
import requests

# دالة /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلا وسهلا! أرسل رابط فيديو تيكتوك الذي تريد تحميله.")

# دالة لتحميل الفيديو
async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    try:
        # تحميل الفيديو بدون علامة مائية
        with TikTokApi() as api:
            video_data = api.video(url=url).bytes()

        # حفظ الفيديو مؤقتًا
        filename = "video.mp4"
        with open(filename, "wb") as f:
            f.write(video_data)

        # إرسال الفيديو للمستخدم
        await update.message.reply_video(video=open(filename, "rb"))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(7535485147:AAHMMqHUQmLqa_ePa3-BeRfaqUXSqm8S1TY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_tiktok))

    print("البوت يعمل الآن...")
    app.run_polling()
