# CVB/handlers/fun_handler.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import random

router = Router()

JOKES = [
    "Why did Bitcoin break up with the dollar? Too volatile!",
    "My wallet told me a joke… but it had no funds.",
    "Why do crypto traders never get lost? Because they follow the charts!"
]

@router.message(Command("joke"))
async def joke_handler(message: Message):
    await message.reply(random.choice(JOKES))