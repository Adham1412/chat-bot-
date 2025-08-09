import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("BOT_TOKEN")

async def greet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        user_firstname = update.message.from_user.first_name
        await update.message.reply_text(f"Salom {user_firstname} 👋")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, greet))
    app.run_polling()

if __name__ == "__main__":
    main()
