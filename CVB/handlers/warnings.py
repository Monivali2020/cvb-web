from aiogram import Router, F
from aiogram.types import Message
from ..models.warnings_model import add_warning, get_warnings, reset_warnings

router = Router()

@router.message(F.command("warn") & F.reply)
async def warn_user(message: Message):
    target = message.reply_to_message.from_user
    count  = add_warning(message.chat.id, target.id)
    await message.reply(f"⚠️ {target.full_name} now has {count} warning(s).")

@router.message(F.command("warns") & F.reply)
async def show_warnings(message: Message):
    target = message.reply_to_message.from_user
    count  = get_warnings(message.chat.id, target.id)
    await message.reply(f"ℹ️ {target.full_name} has {count} warning(s).")

@router.message(F.command("resetwarns") & F.reply)
async def reset_user_warnings(message: Message):
    target = message.reply_to_message.from_user
    reset_warnings(message.chat.id, target.id)
    await message.reply(f"✅ Warnings reset for {target.full_name}.")