# CVB/handlers/security.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from CVB.utils.permissions import is_admin

router = Router()

@router.message(Command("lock"))
async def lock_feature(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id, message.bot):
        await message.reply("❌ You don't have permission to lock features.")
        return
    await message.reply("🔒 Feature locked (simulated).")

@router.message(Command("unlock"))
async def unlock_feature(message: Message):
    if not await is_admin(message.chat.id, message.from_user.id, message.bot):
        await message.reply("❌ You don't have permission to unlock features.")
        return
    await message.reply("🔓 Feature unlocked (simulated).")