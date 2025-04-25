# CVB/handlers/automated.py

from aiogram import Router, F
from aiogram.types import Message
from ..utils.scheduler import schedule_task

router = Router()

# 1) Auto-delete scam keywords via a single regexp filter
SCAM_RE = rf"(?i)({'|'.join(['airdrop','free eth','claim reward','investment scheme'])})"

@router.message(F.text.regexp(SCAM_RE))
async def auto_moderation_handler(message: Message):
    """Delete common scam messages."""
    await message.delete()
    await message.answer("⚠️ Scam message deleted automatically.")

# 2) A catch-all scheduler example
@router.message()  
async def auto_task(message: Message):
    """Example: schedule a background task on any incoming message."""
    await schedule_task(chat_id=message.chat.id, task_data={"user": message.from_user.id})