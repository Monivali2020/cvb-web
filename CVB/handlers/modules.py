from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()
NOTE_STORAGE: dict[int, str] = {}

@router.message(Command("setnote"))
async def set_note(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply("Usage: /setnote <your note>")
        return

    NOTE_STORAGE[message.from_user.id] = parts[1]
    await message.reply("📝 Note saved.")

@router.message(Command("getnote"))
async def get_note(message: Message):
    note = NOTE_STORAGE.get(message.from_user.id)
    if note:
        await message.reply(f"📝 Your Note:\n\n{note}")
    else:
        await message.reply("No note found. Use `/setnote` to create one.", parse_mode="Markdown")