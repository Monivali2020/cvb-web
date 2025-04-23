# CVB/handlers/deposit_handler.py

from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from ..utils.nowpayment import create_invoice

router = Router()

@router.message(Command("deposit"))
async def deposit_handler(message: Message):
    user_id = message.from_user.id
    amount  = 5.00   # default deposit; make dynamic later if you want

    # create_invoice(user_id: int, amount: float) -> dict with "invoice_url"
    payment = create_invoice(user_id, amount)
    pay_url = payment.get("invoice_url")

    if pay_url:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Pay with NowPayment", url=pay_url)]
        ])
        await message.reply(
            f"🧾 <b>Deposit Instructions</b>\n\n"
            f"Amount: <b>${amount:.2f}</b>\n\n"
            "Click below to proceed securely via NowPayments.",
            reply_markup=keyboard,
            parse_mode="HTML"
        )
    else:
        await message.reply("❌ Failed to create invoice. Please try again later.")