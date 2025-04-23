from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

MODULES = [
    "moderation", "security", "fun", "payments", "ai", "wallet",
    "clean/keep", "gban", "warn", "tips", "charts", "filters"
]

@router.message(Command("modules"))
async def list_modules(message: Message):
    module_text = "**Available Modules:**\n\n"
    module_text += "\n".join([f"• {m.title()}" for m in MODULES])
    await message.reply(module_text, parse_mode="Markdown")