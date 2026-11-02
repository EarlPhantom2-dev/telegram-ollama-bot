import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MODEL = os.getenv("OLLAMA_MODEL", "llama2-uncensored:7b")
TIMEOUT = float(os.getenv("OLLAMA_TIMEOUT", "120"))

SYSTEM_PROMPT = """Jawab singkat dan padat. Langsung ke inti. Jangan bertele-tele.
Gunakan 1-3 kalimat max. Hindari penjelasan berlebih."""



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Aku bot AI powered by Ollama.\n"
        f"Model: {MODEL}\n"
        "Kirim pesan, aku balas."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": MODEL,
                    "prompt": f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:",
                    "stream": False,
                    "keep_alive": "10m",
                    "num_predict": 128,
                    "top_k": 40,
                    "top_p": 0.9,
                    "temperature": 0.5,
                },
            )

        if response.status_code != 200:
            logger.error(f"Ollama {response.status_code}: {response.text[:500]}")
            await update.message.reply_text("Error dari Ollama. Coba lagi.")
            return

        result = response.json()
        ai_response = result.get("response", "").strip()
        if not ai_response:
            ai_response = "Tidak ada respons dari model."
        await update.message.reply_text(ai_response[:4096])

    except httpx.TimeoutException:
        logger.warning("Ollama timeout")
        await update.message.reply_text("Timeout. Model sedang loading. Coba lagi.")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(f"Error: {e}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update error: {context.error}", exc_info=context.error)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    app.add_error_handler(error_handler)

    logger.info(f"Bot dimulai... model={MODEL} ollama={OLLAMA_URL}")
    app.run_polling()


if __name__ == "__main__":
    main()
