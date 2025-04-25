# CVB/handlers/user_utils_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("userinfo"))
async def userinfo_handler(message: Message):
    user = message.from_user
    text = (
        f"🧾 <b>User Info</b>\n"
        f"• ID: <code>{user.id}</code>\n"
        f"• Name: {user.full_name}\n"
        f"• Username: @{user.username or 'N/A'}"
    )
    await message.reply(text, parse_mode="HTML")