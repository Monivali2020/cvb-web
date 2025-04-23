import os
import certifi  # <- ADD THIS
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# --- MongoDB setup ---
MONGO_URL = os.getenv("MONGO_URL")
mongo_client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())  # <- FIX IS HERE
mongo_db = mongo_client.get_default_database()

# Collections
warnings_coll = mongo_db.get_collection("warnings")
group_settings_coll = mongo_db.get_collection("group_settings")

# --- SQLAlchemy setup (optional) ---
POSTGRES_URL = os.getenv("POSTGRES_URL") or os.getenv("SQLITE_URL")
engine = create_engine(POSTGRES_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)