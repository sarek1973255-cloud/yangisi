import logging
from flask import Flask
from threading import Thread

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from logic import search_by_oked

# ---------------- BOT TOKEN ----------------
TOKEN = "YOUR_BOT_TOKEN"

logging.basicConfig(level=logging.INFO)

# ---------------- KEEP ALIVE (Replit) ----------------
web_app = Flask("")

@web_app.route("/")
def home():
    return "Bot is alive"

def run_web():
    web_app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

keep_alive()

# ---------------- TELEGRAM BOT ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 OKED kod yuboring\nMasalan: 62010")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("⏳ Qidiryapman...")

    results = search_by_oked(text)

    if not results:
        await update.message.reply_text("❌ Hech narsa topilmadi")
        return

    msg = "🏢 Natijalar:\n\n"

    for r in results[:10]:
        msg += f"{r[0]}\n{r[1]}\n\n"

    await update.message.reply_text(msg)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

app.run_polling(drop_pending_updates=True)
