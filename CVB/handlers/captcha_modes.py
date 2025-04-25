# CVB/handlers/captcha_modes.py

import asyncio
from aiogram import Router, F
from aiogram.types import ChatMemberUpdated, Message
from ..utils.captcha import generate_captcha

router = Router()

# Listen for any chat_member update where the user just became a member
@router.chat_member(F.chat_member.new_chat_member.status == "member")
async def captcha_on_join(event: ChatMemberUpdated):
    """When someone joins, send them a simple captcha challenge."""
    user = event.new_chat_member.user
    chat = event.chat

    # Send the captcha question
    msg: Message = await chat.send_message(
        f"👤 Welcome {user.full_name}! Please solve this captcha in 60s:\n\nWhat is 2 + 2?"
    )

    # Optionally generate & store the answer somewhere:
    # correct_answer = generate_captcha()

    # Wait 60 seconds, then delete the prompt
    await asyncio.sleep(60)
    await msg.delete()