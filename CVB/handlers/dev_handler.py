# handler/dev_handler.py

import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

print(f"Raw ADMIN_IDS from env: '{os.getenv('ADMIN_IDS', '')}'")  # Add this line
ADMINS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x]

@router.message(Command("dev"))
async def dev_command(message: Message):
    if message.from_user.id not in ADMINS:
        return await message.reply("🚫 Access denied.")
    await message.reply("🛠 Dev mode active. Run custom diagnostics here.")