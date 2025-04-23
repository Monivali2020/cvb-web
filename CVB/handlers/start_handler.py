# CVB/handlers/start_handler.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
import os

router = Router()

BOT_USERNAME = os.getenv("BOT_USERNAME", "CryptoValBot")
BASE_URL = os.getenv("BASE_URL", "https://your-dashboard-url.com")
CVB_PINKSALE_LINK = os.getenv("CVB_PINKSALE_LINK", "https://www.pinksale.finance")

@router.message(CommandStart())
async def start_command_handler(message: Message):
    user_mention = message.from_user.mention_html()
    if message.chat.type == "private":
        text = (
            f"Hello {user_mention}, I'm <b>CryptoValBot</b> — your all-in-one crypto & AI assistant.\n\n"
            "• Real-time crypto prices\n"
            "• Pinksale raid support\n"
            "• AI-powered market insights\n"
            "• Secure crypto wallets & payment tools\n\n"
            "Use /help to view all commands!"
        )

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Add to Group", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [InlineKeyboardButton(text="Dashboard", url=BASE_URL)],
            [InlineKeyboardButton(text="PinkSale", url=CVB_PINKSALE_LINK)]
        ])
        await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

    elif message.chat.type in ["group", "supergroup"]:
        await message.reply(
            f"Hello {user_mention}, I'm active in this group!\nUse /help to explore my features.",
            parse_mode="HTML"
        )