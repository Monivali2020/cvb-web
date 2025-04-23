# CVB/models/warnings_model.py

from .db import warnings_coll

def add_warning(chat_id: int, user_id: int) -> int:
    """
    Atomically increment the count by 1 in the warnings collection.
    """
    warnings_coll.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$inc": {"count": 1}},
        upsert=True
    )
    doc = warnings_coll.find_one({"chat_id": chat_id, "user_id": user_id})
    return doc.get("count", 0)

def get_warnings(chat_id: int, user_id: int) -> int:
    doc = warnings_coll.find_one({"chat_id": chat_id, "user_id": user_id})
    return doc.get("count", 0)

def reset_warnings(chat_id: int, user_id: int):
    warnings_coll.update_one(
        {"chat_id": chat_id, "user_id": user_id},
        {"$set": {"count": 0}}
    )