# CVB/handlers/slowmode.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.message(Command("slowmode"))
async def set_slowmode(message: Message):
    try:
        args = message.text.split(maxsplit=1)
        delay = int(args[1]) if len(args) > 1 else 10
        await message.bot.set_chat_slow_mode_delay(message.chat.id, delay)
        await message.reply(f"⏱ Slowmode set to {delay} seconds.")
    except TelegramBadRequest:
        await message.reply("❌ Failed to set slowmode. Make sure I'm admin.")
    except Exception:
        await message.reply("Usage: /slowmode <delay in seconds>")