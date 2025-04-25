# CVB/handlers/tip_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("tips"))
async def tips_handler(message: Message):
    tips_text = (
        "**CryptoVal Tips for Beginners**\n\n"
        "1. **Don't share your private keys.** Ever.\n"
        "2. **Use trusted platforms** like Binance, OKX, Trust Wallet.\n"
        "3. Always **double-check contract addresses** before investing.\n"
        "4. Join our channel for daily crypto alerts.\n"
        "5. Use `/price <token>` to track crypto prices.\n"
        "6. DYOR = Do Your Own Research before buying any token.\n\n"
        "**More educational tips will be added soon!**"
    )
    await message.reply(tips_text, parse_mode="Markdown")