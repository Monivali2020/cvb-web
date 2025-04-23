# utils/permissions.py

import os
from aiogram import Bot

# Static global admin check
ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")

def is_admin(user_id: str) -> bool:
    return user_id in ADMIN_IDS

# Dynamic group admin check
async def is_group_admin(chat_id: int, user_id: int, bot: Bot) -> bool:
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.is_chat_admin()
    except Exception:
        return False