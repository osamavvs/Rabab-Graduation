import os
import subprocess
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# التوكن من متغيرات البيئة
TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")

# تفعيل التسجيل
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 مرحباً في أداة اختبار التحمل الدفاعية!\n\n"
        "الأوامر المتاحة:\n"
        "/test <URL> - تشغيل اختبار تحمل على الموقع المحدد\n"
        "/status - عرض حالة الاختبارات الجارية\n"
        "/help - عرض المساعدة"
    )

async def run_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("⚠️ الرجاء إدخال رابط الموقع: /test https://example.com")
        return
    
    url = context.args[0]
    await update.message.reply_text(f"🔄 جاري تشغيل اختبار التحمل على {url} ...")
    
    try:
        # تشغيل Locust في وضع Headless
        result = subprocess.run([
            "locust", "-f", "locustfile.py",
            "--host", url,
            "--users", "50",
            "--spawn-rate", "10",
            "--run-time", "30s",
            "--headless",
            "--html", "reports/report.html"
        ], capture_output=True, text=True, timeout=60)
        
        # قراءة التقرير وإرساله
        with open("reports/report.html", "r", encoding="utf-8") as f:
            report_content = f.read()[:4000]  # حدود التليجرام
        
        await update.message.reply_text(
            f"✅ اكتمل الاختبار!\n"
            f"📊 النتائج:\n{report_content[:500]}\n\n"
            f"📁 التقرير الكامل في مستودع GitHub"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("test", run_test))
    
    print("🤖 البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
