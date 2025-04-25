# CVB/core/app_instance.py

from pyrogram import Client
from CVB.config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "CryptoValBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)