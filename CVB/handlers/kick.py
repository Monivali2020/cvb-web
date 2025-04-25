# CVB/handlers/kick.py

from aiogram import Router, F
from aiogram.types import Message, ChatMemberUpdated
from aiogram.exceptions import TelegramForbiddenError
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

@router.message(F.text.startswith("/kick"))
async def kick_user(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("🚫 You don't have permission.")

    if not message.reply_to_message:
        return await message.reply("❗Reply to the user you want to kick.")

    try:
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.bot.unban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
        await message.reply("✅ User kicked.")
    except TelegramForbiddenError:
        await message.reply("❌ I don't have permission to kick users.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

    # Auto delete command if clean is enabled
    if await is_clean_enabled(message.chat.id):
        try:
            await message.delete()
        except:
            pass