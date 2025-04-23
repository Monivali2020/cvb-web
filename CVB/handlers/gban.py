# CVB/handlers/gban.py

from aiogram import Router, F
from aiogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient
from ..config import MONGO_URL, ADMIN_IDS

router = Router()

# MongoDB Setup
mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client.CVB
gban_collection = db.gban_users

# Helper function
async def is_admin(user_id: int):
    return str(user_id) in ADMIN_IDS.split(',')

@router.message(F.text.startswith('/gban'))
async def gban_user_handler(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You’re not allowed to use this command.")
    
    if not message.reply_to_message:
        return await message.reply("Reply to the user you want to gban.")

    target = message.reply_to_message.from_user.id
    reason = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else "No reason provided"

    # Save to MongoDB
    await gban_collection.update_one(
        {'user_id': target},
        {'$set': {'reason': reason}},
        upsert=True
    )

    await message.reply(f"Globally banned user: `{target}`\nReason: {reason}")

@router.message(F.text.startswith('/ungban'))
async def ungban_user_handler(message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply("You’re not allowed to use this command.")
    
    if not message.reply_to_message:
        return await message.reply("Reply to the user you want to ungban.")

    target = message.reply_to_message.from_user.id

    await gban_collection.delete_one({'user_id': target})
    await message.reply(f"User `{target}` has been globally unbanned.")