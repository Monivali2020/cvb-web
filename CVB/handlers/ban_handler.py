from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.chat_member_status import ChatMemberStatus

router = Router()

@router.message(Command("ban"))
async def ban_user(message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to the user you want to ban.")
        return

    user_to_ban = message.reply_to_message.from_user.id
    await message.chat.ban(user_to_ban)
    await message.reply(f"User <b>{user_to_ban}</b> has been banned.", parse_mode="HTML")