# CVB/handlers/price_handler.py

import logging
import json
import urllib.parse
import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..config import QUICKCHART_BASE_URL
from ..utils.coingecko import get_token_price

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("price"))
async def price_handler(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply(
            "Please provide a token name.\nExample: `/price bitcoin`",
            parse_mode="Markdown"
        )

    token = parts[1].lower()
    price = await get_token_price(token)
    if price is None:
        return await message.reply(f"Couldn't fetch price for '{token}'. Check token name.")

    # Build a quick line chart of the single latest price (optional)
    chart_config = {
        "type": "doughnut",
        "data": {
            "labels": [token.upper()],
            "datasets": [{"data": [price]}]
        },
        "options": {
            "plugins": {"title": {"display": True, "text": f"{token.upper()} Price (USD)" }}
        }
    }
    raw     = json.dumps(chart_config)
    encoded = urllib.parse.quote_plus(raw)
    chart_url = f"{QUICKCHART_BASE_URL}?c={encoded}&backgroundColor=black&format=png"

    logger.info("QuickChart Price URL → %s", chart_url)
    await message.reply_photo(photo=chart_url, caption=f"💲 {token.capitalize()}: ${price:,.2f}")