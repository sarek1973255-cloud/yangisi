import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from logic import search_all

TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 OKED yuboring (masalan: 62010)")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("⏳ Qidiryapman...")

    results = search_all(text)

    if not results:
        await update.message.reply_text("❌ Hech narsa topilmadi")
        return

    msg = "🏢 Natijalar:\n\n"

    for r in results[:15]:
        msg += f"{r[0]}\n{r[1]}\n\n"

    await update.message.reply_text(msg)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling()
