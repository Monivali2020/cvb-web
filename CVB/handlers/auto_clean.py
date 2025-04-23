# CVB/handlers/auto_clean.py

from aiogram import Router, F
from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGO_URL, ADMIN_IDS

router = Router()
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
clean_settings = db.clean_commands

# Helpers
async def is_admin(user_id):
    return str(user_id) in ADMIN_IDS.split(',')

async def is_clean_enabled(chat_id):
    doc = await clean_settings.find_one({"chat_id": chat_id})
    return doc and doc.get("enabled", False)

@router.message(F.text == "/cleancommand")
async def enable_clean(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You don't have permission to use this command.")
    
    await clean_settings.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"enabled": True}},
        upsert=True
    )
    await message.reply("Clean commands enabled for this group.")

@router.message(F.text == "/keepcommand")
async def disable_clean(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You don't have permission to use this command.")
    
    await clean_settings.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"enabled": False}},
        upsert=True
    )
    await message.reply("Bot will now keep command messages.")

# Middleware-like handler to auto-delete bot commands if cleaning is enabled
@router.message(F.text.startswith("/"))
async def auto_delete_commands(message: Message):
    if await is_clean_enabled(message.chat.id):
        try:
            await message.delete()
        except Exception:
            pass  # Bot might lack permission