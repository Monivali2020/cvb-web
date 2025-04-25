# CVB/handlers/auto_clean.py

import os                                     # ← keep if you ever load env here
from aiogram import Router, F
from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGO_URL, ADMIN_IDS

router = Router()
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
clean_settings = db.clean_commands

async def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS

async def is_clean_enabled(chat_id: int) -> bool:
    doc = await clean_settings.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))

# Enable clean mode
@router.message(F.text == "/cleancommand")
async def enable_clean(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You don't have permission.")
    await clean_settings.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"enabled": True}},
        upsert=True
    )
    await message.reply("✅ Clean commands enabled.")

# Disable clean mode
@router.message(F.text == "/keepcommand")
async def disable_clean(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You don't have permission.")
    await clean_settings.update_one(
        {"chat_id": message.chat.id},
        {"$set": {"enabled": False}},
        upsert=True
    )
    await message.reply("✅ Bot will keep command messages.")

# Auto-delete any other slash-command when clean is enabled
@router.message(F.text.regexp(r"^/"))
async def auto_delete_commands(message: Message):
    if await is_clean_enabled(message.chat.id):
        try:
            await message.delete()
        except:
            pass