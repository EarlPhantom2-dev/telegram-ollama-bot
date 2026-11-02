import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Aku bot AI powered by Ollama.\n"
        "Kirim pesan, aku balas dengan model llama2-uncensored:7b"
    )

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat_action("typing")

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama2-uncensored:7b",
                "prompt": user_message,
                "stream": False
            },
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result.get("response", "Tidak ada respons")
            await update.message.reply_text(ai_response[:4096])
        else:
            await update.message.reply_text("Error dari Ollama. Coba lagi.")
    except requests.exceptions.Timeout:
        await update.message.reply_text("Timeout. Model sedang loading.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error: {str(e)}")

async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    logger.info("Bot dimulai...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
