from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..utils.permissions import is_admin

router = Router()

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("❌ You don't have permission to use this.")
        return

    if not message.reply_to_message:
        await message.reply("Reply to a user to ban them.")
        return

    try:
        await message.bot.ban_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id
        )
        await message.reply("✅ User has been banned.")
    except Exception as e:
        await message.reply(f"Error banning user: {e}")


@router.message(Command("mute"))
async def mute_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("❌ You don't have permission to mute.")
        return

    if not message.reply_to_message:
        await message.reply("Reply to a user to mute them.")
        return

    try:
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions={"can_send_messages": False}
        )
        await message.reply("🔇 User has been muted.")
    except Exception as e:
        await message.reply(f"Error muting user: {e}")


@router.message(Command("unmute"))
async def unmute_user(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id):
        await message.reply("❌ You don't have permission to unmute.")
        return

    if not message.reply_to_message:
        await message.reply("Reply to a user to unmute them.")
        return

    try:
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=message.reply_to_message.from_user.id,
            permissions={"can_send_messages": True}
        )
        await message.reply("🔈 User has been unmuted.")
    except Exception as e:
        await message.reply(f"Error unmuting user: {e}")