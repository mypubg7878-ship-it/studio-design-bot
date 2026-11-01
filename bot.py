
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = os.getenv("OWNER_CHAT_ID")

keyboard = [
    ["🎨 نمونه‌کارها", "📝 ثبت سفارش"],
    ["💰 قیمت‌ها", "📞 ارتباط با ما"],
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 به استودیو طراحی خوش آمدید!\n\n"
        "از منوی زیر یکی از گزینه‌ها را انتخاب کنید:",
        reply_markup=ReplyKeyboardMarkup(
            keyboard, resize_keyboard=True
        )
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🎨 نمونه‌کارها":
        await update.message.reply_text(
            "برای دیدن نمونه‌کارها به سایت ما سر بزنید:\n"
            "https://mypubg7878-ship-it.github.io/logo_studio-/"
        )

    elif text == "📝 ثبت سفارش":
        context.user_data["waiting_order"] = True
        await update.message.reply_text(
            "لطفاً نوع طراحی موردنظرتان را بنویسید."
        )

    elif text == "💰 قیمت‌ها":
        await update.message.reply_text(
            "قیمت طراحی با توجه به نوع و جزئیات سفارش مشخص می‌شود."
        )

    elif text == "📞 ارتباط با ما":
        await update.message.reply_text(
            "برای ارتباط مستقیم پیام بدهید:\nhttps://t.me/ali_ataiw"
        )

    elif context.user_data.get("waiting_order"):
        if OWNER_ID:
            await context.bot.send_message(
                chat_id=int(OWNER_ID),
                text=f"📩 سفارش جدید:\n{text}"
            )
            await update.message.reply_text("سفارش شما ثبت شد. سپاسگزاریم ❤️")
        else:
            await update.message.reply_text(
                "برای تکمیل سفارش به این آدرس پیام بدهید:\n"
                "https://t.me/ali_ataiw"
            )
        context.user_data["waiting_order"] = False

    else:
        await update.message.reply_text(
            "لطفاً یکی از گزینه‌های منو را انتخاب کنید."
        )

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده است")

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

