# CVB/handlers/gban.py

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGO_URL, ADMIN_IDS

router = Router()

# MongoDB Setup
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
gban_collection = db.gban_users

# Helper to check admin
async def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS

@router.message(Command("gban"))
async def gban_user_handler(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You’re not allowed to use this command.")

    if not message.reply_to_message:
        return await message.reply("Reply to the user you want to gban.")

    target = message.reply_to_message.from_user.id
    parts = message.text.split(maxsplit=1)
    reason = parts[1] if len(parts) > 1 else "No reason provided"

    await gban_collection.update_one(
        {"user_id": target},
        {"$set": {"reason": reason}},
        upsert=True
    )

    await message.reply(f"Globally banned user: `{target}`\nReason: {reason}", parse_mode="Markdown")

@router.message(Command("ungban"))
async def ungban_user_handler(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You’re not allowed to use this command.")

    if not message.reply_to_message:
        return await message.reply("Reply to the user you want to ungban.")

    target = message.reply_to_message.from_user.id
    await gban_collection.delete_one({"user_id": target})
    await message.reply(f"User `{target}` has been globally unbanned.", parse_mode="Markdown")