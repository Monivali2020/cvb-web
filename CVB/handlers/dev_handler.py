import os
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

ADMINS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",")]

@router.message(Command("dev"))
async def dev_command(message: Message):
    if message.from_user.id in ADMINS:
        await message.reply("🛠 Dev mode active. Run custom diagnostics here.")
    else:
        await message.reply("Access denied.")