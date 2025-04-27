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
    help_text = (
        f"{bold('CryptoValBot Command Menu')}\n\n"
        f"{bold('Crypto Tools:')}\n"
        f"{code('/price <coin>')} – Get any crypto’s price\n"
        f"{code('/globalchart')} – Global market bar chart\n"
        f"{code('/btcprice')} / {code('/ethtrend')} – Price trend charts\n\n"
        f"{bold('Pinksale Tools:')}\n"
        f"{code('/raid <link>')} – Summon a Pinksale raid\n\n"
        f"{bold('AI & Insights:')}\n"
        f"{code('/ask <question>')} – Ask CryptoValBot anything\n\n"
        f"{bold('Moderation:')}\n"
        f"{code('/cleancommand')} / {code('/keepcommand')} – Command cleaning modes\n\n"
        f"{bold('Other:')}\n"
        f"{code('/wallet')} – Wallet & payment links\n"
        f"{code('/tips')}   – Quick crypto tips\n"
        f"{code('/uptime')} – Bot uptime\n"
    )

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Add to Group",
                url=f"https://t.me/{os.getenv('BOT_USERNAME')}?startgroup=true"
            )
        ],
        [
            InlineKeyboardButton(
                text="Dashboard",
                url=os.getenv("BASE_URL")
            )
        ],
        [
            InlineKeyboardButton(
                text="PinkSale",
                url=os.getenv("CVB_PINKSALE_LINK")
            )
        ],
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    await message.answer(
        help_text,
        parse_mode="Markdown",
        reply_markup=keyboard
    )