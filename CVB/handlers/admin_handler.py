# CVB/handlers/admin_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..utils.permissions import is_admin  # ✅ Checks against your ADMIN_IDS inside that util

router = Router()

@router.message(Command("admin"))
async def admin_panel(message: Message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        return await message.reply("❌ You are not an admin.")

    msg = (
        "**CryptoValBot Admin Panel**\n\n"
        "**Global Tools:**\n"
        "`/gban` – Global ban (reply)\n"
        "`/ungban` – Remove global ban\n\n"
        "**Bot Tools:**\n"
        "`/cleancommand` – Clean mode\n"
        "`/keepcommand` – Keep command replies\n"
        "`/ban`, `/unban` – Local group moderation\n"
        "`/stats` – Get bot stats\n\n"
        "_More features coming soon..._"
    )
    await message.reply(msg, parse_mode="Markdown")