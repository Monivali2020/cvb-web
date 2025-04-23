from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("threads"))
async def threads_handler(message: Message):
    await message.reply("Thread support coming soon. Stay tuned!")