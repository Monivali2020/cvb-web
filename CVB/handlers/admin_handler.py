from aiogram import Router, F
from aiogram.types import Message
from ..config import ADMIN_IDS
from ..utils.permissions import is_admin  # ✅ Utility import

router = Router()

@router.message(F.text == "/admin")
async def admin_panel(message: Message):
    if not is_admin(str(message.from_user.id)):
        return await message.reply("You are not an admin.")

    msg = (
        "**CryptoValBot Admin Panel**\n\n"
        "**Global Tools:**\n"
        "`/gban` - Global ban (reply)\n"
        "`/ungban` - Remove global ban\n\n"
        "**Bot Tools:**\n"
        "`/cleancommand` - Clean mode\n"
        "`/keepcommand` - Keep command replies\n"
        "`/ban`, `/unban` - Local group moderation\n"
        "`/stats` - Get bot stats\n\n"
        "_More features coming soon..._"
    )
    await message.reply(msg, parse_mode="Markdown")