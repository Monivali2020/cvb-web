from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("ping"))
async def ping_handler(message: Message):
    await message.reply("🏓 Pong!")

@router.message(Command("id"))
async def id_handler(message: Message):
    user = message.from_user
    await message.reply(f"👤 Your Telegram ID: <code>{user.id}</code>", parse_mode="HTML")