# CVB/handlers/price_handler.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from ..utils.coingecko import get_token_price

router = Router()

@router.message(Command("price"))
async def price_handler(message: Message):
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply("Please provide a token name.\nExample: /price bitcoin")
        return

    token = args[1].lower()
    price = await get_token_price(token)

    if price is None:
        await message.reply(f"Couldn't fetch price for '{token}'. Check token name.")
    else:
        await message.reply(f"Current price of <b>{token.capitalize()}</b> is <b>${price:,.2f}</b>", parse_mode="HTML")