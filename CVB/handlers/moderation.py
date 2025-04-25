# CVB/handlers/moderation.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from ..utils.permissions import is_admin  # assume this is an async fn

router = Router()

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("❌ You don't have permission to use this.")

    if not message.reply_to_message:
        return await message.reply("Reply to a user to ban them.")

    user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.ban(user_id)
        await message.reply("✅ User has been banned.")
    except Exception as e:
        await message.reply(f"Error banning user: {e}")

@router.message(Command("mute"))
async def mute_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("❌ You don't have permission to mute.")

    if not message.reply_to_message:
        return await message.reply("Reply to a user to mute them.")

    user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.restrict(
            user_id,
            can_send_messages=False
        )
        await message.reply("🔇 User has been muted.")
    except Exception as e:
        await message.reply(f"Error muting user: {e}")

@router.message(Command("unmute"))
async def unmute_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        return await message.reply("❌ You don't have permission to unmute.")

    if not message.reply_to_message:
        return await message.reply("Reply to a user to unmute them.")

    user_id = message.reply_to_message.from_user.id
    try:
        await message.chat.restrict(
            user_id,
            can_send_messages=True
        )
        await message.reply("🔈 User has been unmuted.")
    except Exception as e:
        await message.reply(f"Error unmuting user: {e}")