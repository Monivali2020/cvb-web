# CVB/handlers/raid_handler.py

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from ..config import CVB_PINKSALE_LINK

router = Router()

@router.message(Command("raid"))
async def raid_handler(message: Message):
    raid_text = (
        "**CryptoVal Raid Instructions**\n\n"
        "Want to boost a crypto campaign or presale?\n\n"
        "**Steps:**\n"
        "1. Join the project group\n"
        "2. Use viral messages (copy/paste)\n"
        "3. Spam during peak hours\n"
        "4. Tag admins to boost visibility\n\n"
        "**Presale Link:**\n"
        f"[Click here to view on PinkSale]({CVB_PINKSALE_LINK})\n\n"
        "_This feature will support automated raid scheduling in future updates._"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Open PinkSale", url=CVB_PINKSALE_LINK)
            ]
        ]
    )
    await message.reply(raid_text, parse_mode="Markdown", disable_web_page_preview=True)