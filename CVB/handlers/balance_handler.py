#handler/balance_handler.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from CVB.models.wallet_model import get_or_create_wallet

router = Router()

@router.message(Command("balance"))
async def balance_handler(message: Message):
    user_id = message.from_user.id
    wallet  = get_or_create_wallet(user_id)
    balance = wallet["balance"]
    await message.reply(
        f"💰 Your wallet balance is: <b>${balance:.2f}</b>",
        parse_mode="HTML",
    )