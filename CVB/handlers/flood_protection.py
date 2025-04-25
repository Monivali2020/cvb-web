# CVB/handlers/flood_handler.py

from aiogram import Router, F
from aiogram.types import Message

router = Router()

# Example flood protection: delete messages with too many caps
@router.message(F.text.matches(r'^[^a-z]*$'))  # all-caps messages
async def delete_all_caps(message: Message):
    try:
        await message.delete()
    except:
        pass  # missing permissions? ignore