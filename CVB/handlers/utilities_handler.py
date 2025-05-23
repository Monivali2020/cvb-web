# CVB/handlers/utilities_handler.py

import time
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from ..config import BOT_START_TIME

router = Router()

@router.message(F.command("uptime"))
async def uptime_handler(message: Message):
    now = int(time.time())
    started = int(BOT_START_TIME.timestamp())
    delta = now - started
    hrs, rem = divmod(delta, 3600)
    mins, secs = divmod(rem, 60)
    await message.reply(f"⏱️ Uptime: {hrs}h {mins}m {secs}s")

@router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "**CryptoValBot Commands:**\n\n"
        "/price `<coin>` — Get crypto price\n"
        "/globalchart — View global market chart\n"
        "/raid — Generate Pinksale raid link\n"
        "/wallet — Show on-chain wallet\n"
        "/tips — Crypto tips for beginners\n"
        "/ask `<question>` — Ask AI market insights\n"
        "/uptime — Bot uptime\n"
        "/balance — Show your wallet balance\n"
        "/deposit — Create a deposit invoice\n"
        "/invoice `<USD>` — NowPayments invoice\n"
        "/paystack `<NGN>` — Paystack invoice\n"
        "/flutterwave `<NGN>` — Flutterwave invoice\n"
        "/warn /warns /resetwarns — Warnings management\n"
        "/ban /unban — Group moderation\n"
    )
    await message.reply(help_text, parse_mode=ParseMode.MARKDOWN)