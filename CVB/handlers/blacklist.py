# CVB/handlers/blacklist.py

from aiogram import Router, F
from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGO_URL

router = Router()
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
clean_settings = db.clean_commands

BLACKLIST = {"scam", "rugpull", "honeypot"}

async def is_clean_enabled(chat_id: int) -> bool:
    doc = await clean_settings.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))

@router.message(F.text)
async def blacklist_check(message: Message):
    text = message.text.lower()
    if any(word in text for word in BLACKLIST):
        try:
            await message.delete()
            if not await is_clean_enabled(message.chat.id):
                await message.answer("❌ That word is not allowed here.")
        except:
            pass