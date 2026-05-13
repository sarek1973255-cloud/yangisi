import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from scraper import search_companies

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OKED kod yubor: masalan 62010")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    oked = update.message.text

    await update.message.reply_text("Qidiryapman...")

    results = search_companies(oked)

    if not results:
        await update.message.reply_text("Hech narsa topilmadi 😕")
        return

    text = "\n\n".join(results)
    await update.message.reply_text(text[:4000])  # limit Telegram

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()