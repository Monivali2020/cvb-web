# CVB/handlers/stats.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("stats"))
async def stats_handler(message: Message):
    await message.reply("📊 Bot Stats:\n- Users: 1,245\n- Groups: 128\n- Running: ✅")