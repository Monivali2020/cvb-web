import logging
import json
import urllib.parse
import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from ..config import QUICKCHART_BASE_URL
from ..utils.coingecko import get_btc_price_history, get_eth_price_history

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("globalchart"))
async def global_chart_handler(message: Message):
    # 1) fetch 7-day histories
    btc_data = await get_btc_price_history(days=7)
    eth_data = await get_eth_price_history(days=7)
    if not btc_data or not eth_data:
        return await message.reply("⚠️ Unable to fetch price history.")

    # 2) prepare labels & data
    labels     = [
        datetime.datetime.fromtimestamp(pt[0] // 1000).strftime("%b %d")
        for pt in btc_data
    ]
    btc_prices = [pt[1] for pt in btc_data]
    eth_prices = [pt[1] for pt in eth_data]

    # 3) build QuickChart JSON config
    chart_config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [
                {"label": "BTC (USD)", "data": btc_prices},
                {"label": "ETH (USD)", "data": eth_prices}
            ]
        },
        "options": {
            "plugins": {
                "title": {"display": True, "text": "7-Day BTC vs ETH (USD)"}
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
    logger.info("QuickChart Global URL → %s", chart_url)

    # 7) send the chart directly
    await message.reply_photo(
        photo=chart_url,
        caption="📊 7-Day BTC vs ETH (USD)",
        parse_mode="HTML"
    )