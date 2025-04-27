import os
import threading
import asyncio
from dotenv import load_dotenv
from CVB.flask_app import app
from CVB.models.wallet_model import init_wallet_db
from CVB.bot import bot

# Load .env
load_dotenv()

# Initialize Wallet DB
init_wallet_db()

def run_flask():
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

async def set_webhook():
    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        await bot.set_webhook(webhook_url)
    else:
        print("WEBHOOK_URL not set!")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    asyncio.run(set_webhook())
    flask_thread.join()