# CVB/handlers/help_handler.py

import os
from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.markdown import bold, code

router = Router()

print(f"BOT_USERNAME: {os.getenv('BOT_USERNAME')}")
print(f"BASE_URL: {os.getenv('BASE_URL')}")
print(f"CVB_PINKSALE_LINK: {os.getenv('CVB_PINKSALE_LINK')}")

@router.message(Command("help", ignore_case=True))
async def help_command(message: Message):
    help_text = f"{bold('CryptoValBot Help Menu')}\n\nHere are some commands:"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Test Button", url="https://www.google.com")
            ]
        ]
    )

    await message.answer(
        help_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )