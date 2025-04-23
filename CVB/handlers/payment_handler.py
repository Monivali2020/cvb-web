# CVB/handlers/payment_handler.py

import os
from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from ..models.wallet_model import get_or_create_wallet, update_wallet_balance
from ..utils.nowpayment    import create_invoice    as create_nowpayment_invoice, \
                                  check_invoice_status
from ..utils.paystack       import create_invoice    as create_paystack_invoice, \
                                  verify_payment      as verify_paystack
from ..utils.flutterwave    import create_invoice    as create_flutterwave_invoice, \
                                  verify_payment      as verify_flutterwave

router = Router()

WALLET_ADDRESS = "0x891201adf9094de2209dc36d141ca710cf76f282"


@router.message(F.command("wallet"))
async def wallet_handler(message: Message):
    """Show on‑chain wallet address with pay buttons."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton("Pay via NowPayment", url=f"https://nowpayments.io/pay/{WALLET_ADDRESS}"),
            InlineKeyboardButton("Etherscan",       url=f"https://etherscan.io/address/{WALLET_ADDRESS}")
        ]
    ])
    await message.reply(
        f"🔗 **Your Wallet Address**\n`{WALLET_ADDRESS}`\n\nChoose a payment method:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@router.message(F.command("invoice"))
async def invoice_handler(message: Message):
    """Create a NowPayment invoice: /invoice <USD amount>."""
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/invoice <USD amount>`", parse_mode="Markdown")

    try:
        amt = float(parts[1])
    except ValueError:
        return await message.reply("Amount must be a number. E.g. `/invoice 15.50`", parse_mode="Markdown")

    data = create_nowpayment_invoice(user_id=message.from_user.id, amount=amt)
    link = data.get("invoice_url")
    if link:
        await message.reply(f"💰 Invoice for ${amt:.2f} → {link}", parse_mode="Markdown")
    else:
        await message.reply(f"❌ Failed: {data.get('error', 'Unknown error')}")


@router.message(F.command("paystack"))
async def paystack_handler(message: Message):
    """Initialize Paystack transaction: /paystack <NGN amount> [email]."""
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/paystack <amount_NGN> [email]`", parse_mode="Markdown")

    try:
        amt = int(parts[1])
    except ValueError:
        return await message.reply("Amount must be an integer. E.g. `/paystack 2000`", parse_mode="Markdown")

    email = parts[2] if len(parts) > 2 else None
    res = create_paystack_invoice(amount_naira=amt, email=email)
    if res.get("status"):
        await message.reply(f"💳 Paystack link → {res['data']['authorization_url']}")
    else:
        await message.reply("❌ Paystack init failed.")


@router.message(F.command("flutterwave"))
async def flutterwave_handler(message: Message):
    """Initialize Flutterwave transaction: /flutterwave <NGN amount>."""
    parts = message.text.split()
    if len(parts) < 2:
        return await message.reply("Usage: `/flutterwave <amount_NGN>`", parse_mode="Markdown")

    try:
        amt = float(parts[1])
    except ValueError:
        return await message.reply("Amount must be a number. E.g. `/flutterwave 1500.50`", parse_mode="Markdown")

    res = create_flutterwave_invoice(amount_naira=amt, user_id=message.from_user.id)
    if res.get("status") == "success":
        await message.reply(f"💳 Flutterwave link → {res['data']['link']}")
    else:
        await message.reply("❌ Flutterwave init failed.")


@router.message(F.command("balance"))
async def balance_handler(message: Message):
    """Show user’s current wallet balance."""
    wallet = get_or_create_wallet(message.from_user.id)
    await message.reply(f"🏦 Your balance: {wallet['balance']}")


@router.message(F.command("invoice_status") & F.reply)
async def invoice_status_handler(message: Message):
    """Verify and credit a NowPayment invoice by replying with its ID."""
    parts = message.text.split()
    invoice_id = parts[1] if len(parts) > 1 else None
    if not invoice_id:
        return await message.reply("Usage: reply `/invoice_status <invoice_id>`", parse_mode="Markdown")

    status = check_invoice_status(invoice_id)
    if status.get("payment_status") == "finished":
        amount = float(status.get("price_amount", 0))
        update_wallet_balance(message.from_user.id, amount)
        await message.reply("✅ Payment confirmed and balance updated.")
    else:
        await message.reply(f"ℹ️ Status: {status.get('payment_status','unknown')}")