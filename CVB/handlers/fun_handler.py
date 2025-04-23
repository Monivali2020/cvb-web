from aiogram import Router, F
from aiogram.types import Message
import random

router = Router()

JOKES = [
    "Why don’t crypto traders tell secrets on elevators? Too many whales.",
    "I tried mining crypto once... now my laptop sounds like a jet engine.",
    "HODL like your life depends on it!"
]

@router.message(F.command("joke"))
async def send_joke(message: Message):
    await message.reply(random.choice(JOKES))