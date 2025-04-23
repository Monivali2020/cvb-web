from aiogram import Router, F
from aiogram.types import Message

router = Router()

BLACKLIST = ["scam", "rugpull", "honeypot"]

@router.message(F.text)
async def blacklist_check(message: Message):
    if any(word in message.text.lower() for word in BLACKLIST):
        await message.delete()
        await message.answer("❌ This word is not allowed.")