# CVB/handlers/gkick_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("gkick"))
async def gkick_handler(message: Message):
    await message.reply("Global kick functionality coming soon.")