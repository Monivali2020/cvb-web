# CVB/handlers/blacklist.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

# List of forbidden words
BLACKLIST = {"scam", "rugpull", "honeypot"}

@router.message(F.text)
async def blacklist_check(message: Message):
    text = message.text.lower()
    if any(word in text for word in BLACKLIST):
        await message.delete()
        await message.answer("❌ That word is not allowed here.")