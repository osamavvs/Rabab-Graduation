import os
import subprocess
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# التوكن من متغيرات البيئة
TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("❌ لم يتم تعيين TELEGRAM_TOKEN في متغيرات البيئة")

# تفعيل التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔒 مرحباً في أداة اختبار التحمل الدفاعية!\n\n"
        "📌 الأوامر المتاحة:\n"
        "/test <URL> - تشغيل اختبار تحمل على الموقع المحدد\n"
        "/status - عرض حالة الاختبارات الجارية\n"
        "/help - عرض المساعدة\n\n"
        "⚠️ للاستخدام التعليمي فقط في بيئات معملية"
    )

async def run_test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "⚠️ الرجاء إدخال رابط الموقع:\n"
            "مثال: /test https://example.com"
        )
        return
    
    url = context.args[0]
    await update.message.reply_text(f"🔄 جاري تشغيل اختبار التحمل على {url} ...")
    
    try:
        # إنشاء مجلد التقارير
        os.makedirs("reports", exist_ok=True)
        
        # تشغيل Locust في وضع Headless
        cmd = [
            "locust", "-f", "locustfile.py",
            "--host", url,
            "--users", "30",
            "--spawn-rate", "5",
            "--run-time", "20s",
            "--headless",
            "--html", "reports/report.html"
        ]
        
        logger.info(f"تشغيل الأمر: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        
        # قراءة التقرير
        report_path = "reports/report.html"
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
            
            # إرسال ملخص (أول 1000 حرف)
            summary = report_content[:1000]
            await update.message.reply_text(
                f"✅ اكتمل الاختبار!\n"
                f"📊 ملخص النتائج:\n{summary[:500]}\n\n"
                f"📁 تم حفظ التقرير الكامل في المستودع"
            )
        else:
            await update.message.reply_text("⚠️ تم الاختبار ولكن لم يتم إنشاء التقرير")
            
    except subprocess.TimeoutExpired:
        await update.message.reply_text("⏰ انتهى وقت الاختبار (45 ثانية)")
    except Exception as e:
        logger.error(f"خطأ: {str(e)}")
        await update.message.reply_text(f"❌ حدث خطأ: {str(e)}")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 البوت يعمل بشكل طبيعي\n"
        "📊 لا توجد اختبارات جارية حالياً"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 المساعدة:\n\n"
        "/test <URL> - تشغيل اختبار تحمل\n"
        "/status - عرض حالة البوت\n"
        "/help - عرض هذه الرسالة\n\n"
        "🔧 مثال: /test https://example.com"
    )

def main():
    """تشغيل البوت"""
    logger.info("🚀 بدء تشغيل البوت...")
    
    # إنشاء التطبيق
    application = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("test", run_test))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("help", help_command))
    
    # تشغيل البوت (Polling)
    logger.info("✅ البوت جاهز للاستخدام!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
