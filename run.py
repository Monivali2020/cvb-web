#!/usr/bin/env python3
import asyncio
import threading
from dotenv import load_dotenv
from CVB.flask_app import app
from CVB.models.wallet_model import init_wallet_db
from CVB.bot import main
import os

# Load .env
load_dotenv()

# Initialize Wallet DB
init_wallet_db()

# === Run Flask app in a thread ===
def run_flask():
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# === Main ===
if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(main())