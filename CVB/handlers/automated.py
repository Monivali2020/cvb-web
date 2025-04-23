from aiogram import Router
from aiogram.types import Message
import re
from ..utils.scheduler import schedule_task

router = Router()

@router.message()
async def auto_moderation_handler(message: Message):
    scam_keywords = ["airdrop", "free eth", "claim reward", "investment scheme"]
    if any(word in message.text.lower() for word in scam_keywords):
        await message.delete()
        await message.chat.send_message("⚠️ Scam message deleted automatically.")

@router.message()  # sample use
async def auto_task(message: Message):
    await schedule_task(chat_id=message.chat.id, task_data="Do something")