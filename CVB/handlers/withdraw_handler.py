from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from ..models.wallet_model import get_or_create_wallet, update_wallet_balance

router = Router()

class WithdrawStates(StatesGroup):
    waiting_for_address = State()
    waiting_for_amount = State()

user_requests = {}

@router.message(Command("withdraw"))
async def withdraw_start(message: Message, state: FSMContext):
    await message.answer("Please send the wallet address where you want to receive your crypto.")
    await state.set_state(WithdrawStates.waiting_for_address)

@router.message(WithdrawStates.waiting_for_address)
async def withdraw_get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("Got it. Now enter the amount you want to withdraw:")
    await state.set_state(WithdrawStates.waiting_for_amount)

@router.message(WithdrawStates.waiting_for_amount)
async def withdraw_get_amount(message: Message, state: FSMContext):
    data = await state.get_data()
    address = data["address"]
    try:
        amount = float(message.text)
        user_id = message.from_user.id
        wallet = get_or_create_wallet(user_id)
        
        if amount > wallet["balance"]:
            await message.answer("Insufficient balance. Try a lower amount.")
            return
        
        update_wallet_balance(user_id, -amount)  # Deduct amount
        await message.answer(
            f"✅ Withdrawal request submitted!\n\n"
            f"Amount: {amount} USDT\n"
            f"Address: {address}\n\n"
            f"Our team will process it shortly."
        )

        print(f"[WITHDRAWAL] User {user_id} requested {amount} to {address}")

        # You could also save this to DB or a CSV later

    except ValueError:
        await message.answer("Invalid amount. Please enter a number.")

    await state.clear()