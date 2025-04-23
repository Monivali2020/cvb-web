# CVB/handlers/filters_handler.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

FILTERS = {
    "bitcoin": "Bitcoin is the first and most valuable cryptocurrency.",
    "eth": "Ethereum is a decentralized platform for smart contracts.",
}

@router.message(Command("filter"))
async def filter_handler(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Usage: /filter <keyword>")
        return

    keyword = args[1].lower()
    response = FILTERS.get(keyword, "No filter found for that keyword.")
    await message.reply(response)