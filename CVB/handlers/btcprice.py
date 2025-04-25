#handler/btcprice.py

import logging
import json
import urllib.parse
import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..config import QUICKCHART_BASE_URL
from ..utils.coingecko import get_btc_price_history

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("btcprice"))
async def btc_chart_handler(message: Message):
    # 1) fetch 7-day history
    history = await get_btc_price_history()
    if not history:
        return await message.reply("⚠️ Couldn't fetch Bitcoin data.")

    # 2) prepare labels & data
    labels = [
        datetime.datetime.fromtimestamp(pt[0] // 1000).strftime("%b %d")
        for pt in history
    ]
    prices = [round(pt[1], 2) for pt in history]

    # 3) build QuickChart JSON config
    chart_config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "BTC/USD",
                "data": prices,
                "borderColor": "orange",
                "fill": False
            }]
        },
        "options": {
            "title": {"display": True, "text": "Bitcoin Price (7d)"},
            "scales": {
                "y": {"beginAtZero": False},
                "x": {"ticks": {"maxRotation": 45, "minRotation": 0}}
            }
        }
    }

    # 4) JSON-dump & percent-encode
    raw     = json.dumps(chart_config)
    encoded = urllib.parse.quote_plus(raw)
    chart_url = (
        f"{QUICKCHART_BASE_URL}"
        f"?c={encoded}"
        "&backgroundColor=black"
        "&format=png"
    )

    # 5) ensure HTTPS
    if chart_url.startswith("http://"):
        chart_url = chart_url.replace("http://", "https://", 1)

    # 6) log for debugging
    logger.info("QuickChart BTC URL → %s", chart_url)

    # 7) send the chart directly
    await message.reply_photo(
        photo=chart_url,
        caption="📈 7-day BTC price trend (USD)",
        parse_mode="HTML"
    )