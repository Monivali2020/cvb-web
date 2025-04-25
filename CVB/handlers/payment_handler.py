# CVB/handlers/payment_handler.py

import logging

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from ..models.wallet_model import get_or_create_wallet, update_wallet_balance
from ..utils.nowpayment import create_invoice as create_nowpayment_invoice, check_invoice_status
from ..utils.paystack import create_invoice as create_paystack_invoice
from ..utils.flutterwave import create_invoice as create_flutterwave_invoice

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("wallet"))
async def onchain_wallet(message: Message):
    WALLET_ADDR = "0x891201adf9094de2209dc36d141ca710cf76f282"
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("Pay via NOWPayments", url=f"https://nowpayments.io/pay/{WALLET_ADDR}"),
            InlineKeyboardButton("View on Etherscan",       url=f"https://etherscan.io/address/{WALLET_ADDR}")
        ]
    ])
    await message.reply(
        f"🔗 **Your Wallet Address**\n`{WALLET_ADDR}`\n\nChoose a payment method:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

@router.message(Command("invoice"))
async def invoice_handler(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Usage: `/invoice <amount_USD>`", parse_mode="Markdown")

    try:
        amt = float(parts[1])
    except ValueError:
        return await message.reply("Amount must be a number. E.g. `/invoice 15.50`", parse_mode="Markdown")

    data = create_nowpayment_invoice(user_id=message.from_user.id, amount=amt)
    link = data.get("invoice_url")
    if link:
        await message.reply(f"💰 Invoice for ${amt:.2f} → {link}", parse_mode="Markdown")
    else:
        await message.reply(f"❌ Failed: {data.get('error', 'Unknown error')}", parse_mode="Markdown")

@router.message(Command("paystack"))
async def paystack_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/paystack <amount_NGN> [email]`", parse_mode="Markdown")

    try:
        amt = int(parts[1])
    except ValueError:
        return await message.reply("Amount must be an integer. E.g. `/paystack 2000`", parse_mode="Markdown")

    email = parts[2] if len(parts) > 2 else None
    res = create_paystack_invoice(amount_naira=amt, email=email)
    url = res.get("data", {}).get("authorization_url")
    if url:
        await message.reply(f"💳 Paystack link → {url}")
    else:
        await message.reply("❌ Paystack init failed.")

@router.message(Command("flutterwave"))
async def flutterwave_handler(message: Message):
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/flutterwave <amount_NGN>`", parse_mode="Markdown")

    try:
        amt = float(parts[1])
    except ValueError:
        return await message.reply("Amount must be a number. E.g. `/flutterwave 1500.50`", parse_mode="Markdown")

    res = create_flutterwave_invoice(amount_naira=amt, user_id=message.from_user.id)
    link = res.get("data", {}).get("link")
    if link:
        await message.reply(f"💳 Flutterwave link → {link}")
    else:
        await message.reply("❌ Flutterwave init failed.")

@router.message(Command("invoice_status"))
async def invoice_status_handler(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        return await message.reply("Usage: `/invoice_status <invoice_id>`", parse_mode="Markdown")

    invoice_id = parts[1]
    status = check_invoice_status(invoice_id)
    if status.get("payment_status") == "finished":
        amt = float(status.get("price_amount", 0))
        update_wallet_balance(message.from_user.id, amt)
        await message.reply("✅ Payment confirmed and balance updated.")
    else:
        await message.reply(f"ℹ️ Status: {status.get('payment_status', 'unknown')}")