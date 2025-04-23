from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("unban"))
async def unban_handler(message: Message):
    if not message.reply_to_message:
        await message.reply("Reply to the user you want to unban.")
        return

    user_to_unban = message.reply_to_message.from_user.id
    await message.chat.unban(user_to_unban)
    await message.reply(f"User <b>{user_to_unban}</b> has been unbanned.", parse_mode="HTML")