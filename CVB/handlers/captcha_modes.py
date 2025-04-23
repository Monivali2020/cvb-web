from aiogram import Router
from aiogram.types import Message, ChatMemberUpdated
import asyncio
from ..utils.captcha import generate_captcha

router = Router()

@router.chat_member()
async def captcha_on_join(event: ChatMemberUpdated):
    if event.new_chat_member.status == "member":
        msg = await event.chat.send_message(
            f"👤 Welcome {event.new_chat_member.user.full_name}! Please solve this captcha within 60s:\n\nWhat is 2 + 2?"
        )
        await asyncio.sleep(60)
        await msg.delete()
        # Logic to check answer — extend with DB if needed