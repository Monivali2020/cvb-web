import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from datetime import datetime
from pymongo import MongoClient
import os

mongo_client = MongoClient(os.getenv("MONGO_URL"))
mongo_db = mongo_client.get_default_database()

# Load .env values
load_dotenv()

# === ENV VARIABLES ===
BOT_TOKEN = os.getenv("CVB_TELE_API")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
LOG_CHANNEL_ID = os.getenv("LOG_CHANNEL_ID")
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")  # Comma-separated admin list

# === Optional: For tracking uptime ===
BOT_START_TIME = datetime.utcnow()

# === Setup Logging ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Initialize Bot and Dispatcher ===
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

from CVB.core.app_instance import app

# === Import Main Routers ===
from .handlers import main_router

dp.include_router(main_router)

# === Optional Middlewares or Filters ===
# from CVB.middlewares.logging_middleware import setup_logging
# setup_logging(dp)

# === Start Bot Function ===
async def main():
    logger.info("Starting CryptoValBot...")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# === Entrypoint ===
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("Bot stopped manually.")