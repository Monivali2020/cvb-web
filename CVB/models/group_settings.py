# CVB/models/group_settings.py

from .wallet_model import db

def get_clean_mode(chat_id: int) -> bool:
    doc = db.group_settings.find_one({"chat_id": chat_id})
    return doc["clean_mode"] if doc else True

def set_clean_mode(chat_id: int, mode: bool):
    db.group_settings.update_one(
        {"chat_id": chat_id},
        {"$set": {"clean_mode": mode}},
        upsert=True
    )