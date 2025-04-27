from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from CVB.models.wallet_model import get_or_create_wallet
from CVB.utils.paystack import create_invoice as create_paystack_invoice
from CVB.utils.nowpayment import create_invoice as create_nowpayments_invoice
from CVB.utils.flutterwave import create_invoice as create_flutterwave_invoice
from CVB.config import MONGO_URL
from motor.motor_asyncio import AsyncIOMotorClient

router = Router()

# Setup MongoDB to check clean command setting
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
clean_settings = db.clean_commands

async def is_clean_enabled(chat_id: int) -> bool:
    doc = await clean_settings.find_one({"chat_id": chat_id})
    return bool(doc and doc.get("enabled", False))

@router.message(Command("wallet"))
async def wallet_handler(message: types.Message):
    if await is_clean_enabled(message.chat.id):
        try:
            await message.delete()
        except:
            pass

    user_id = message.from_user.id
    wallet = get_or_create_wallet(user_id)
    balance = wallet["balance"]

    # Create payment links
    paystack_link = None
    nowpayments_link = None
    flutterwave_link = None

    try:
        paystack_res = create_paystack_invoice(5000, email=str(user_id))
        paystack_link = paystack_res.get("data", {}).get("authorization_url")
    except Exception as e:
        print(f"Paystack error: {e}")

    try:
        now_res = create_nowpayments_invoice(user_id, 10.0)
        nowpayments_link = now_res.get("invoice_url")
    except Exception as e:
        print(f"NOWPayments error: {e}")

    try:
        flutter_res = create_flutterwave_invoice(5000, user_id)
        flutterwave_link = flutter_res.get("data", {}).get("link")
    except Exception as e:
        print(f"Flutterwave error: {e}")

    # Construct inline keyboard
    buttons = []
    if paystack_link:
        buttons.append([InlineKeyboardButton(text="Deposit (NGN) via Paystack", url=paystack_link)])
    if flutterwave_link:
        buttons.append([InlineKeyboardButton(text="Deposit (NGN) via Flutterwave", url=flutterwave_link)])
    if nowpayments_link:
        buttons.append([InlineKeyboardButton(text="Deposit (USDT) via NOWPayments", url=nowpayments_link)])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None

    text = f"**Wallet Overview**\n\nBalance: `${balance:.2f}` USD"

    await message.answer(
        text,
        reply_markup=keyboard,
        parse_mode="Markdown"
    )