#handler/ban_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not message.reply_to_message:
        return await message.reply("⚠️ Please reply to the user you want to ban.")

    to_ban = message.reply_to_message.from_user.id
    await message.chat.ban(to_ban)
    await message.reply(f"🚫 User <b>{to_ban}</b> has been banned.", parse_mode="HTML")