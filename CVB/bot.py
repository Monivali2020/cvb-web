import asyncio
import logging
import os
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from pymongo import MongoClient
from aiogram.client.default import DefaultBotProperties

# Load .env values
load_dotenv()

# === ENV VARIABLES ===
BOT_TOKEN = os.getenv("CVB_TELE_API")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

# === AI INTEGRATIONS ===
GEMINI_API_KEY = os.getenv("CVB_GAPI")
OPENROUTER_API_KEY = os.getenv("CVBAI")
HUGGINGFACE_API_KEY = os.getenv("HCVBHFAI")
META_AI_API_KEY = os.getenv("MAIK")

# === Optional: For tracking uptime ===
BOT_START_TIME = datetime.utcnow()

# === Setup Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Initialize MongoDB ===
mongo_client = MongoClient(os.getenv("MONGO_URL"))
mongo_db = mongo_client.get_default_database()

# === Initialize Bot and Dispatcher ===
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# === Import Main Routers ===
from .handlers import main_router

dp.include_router(main_router)

# === Start Bot Function ===
async def main():
    logger.info("Starting CryptoValBot...")

    # Delete old webhook (important when redeploying)
    await bot.delete_webhook(drop_pending_updates=True)

    # Set new webhook
    from CVB.flask_app import app
    webhook_url = os.getenv("WEBHOOK_URL", "")
    
    if webhook_url:
        await bot.set_webhook(url=webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    else:
        logger.error("WEBHOOK_URL not set in environment!")

    # No polling anymore

# === Entrypoint ===
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")