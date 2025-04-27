import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.webhook.routes import setup_webhook
from aiohttp import web

# Enable basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("CVB_TELE_API")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  # Your public IP or domain
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'  # Listen on all interfaces
WEBAPP_PORT = int(os.getenv("PORT", 8080))      # Choose a port for your web app (Railway uses PORT)

# Initialize bot and dispatcher
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Include your handlers router
from CVB.handlers import main_router
dp.include_router(main_router)

async def on_startup(bot: Bot):
    global WEBHOOK_URL
    log.info(f"WEBHOOK_HOST from env: {WEBHOOK_HOST}")  # Added logging for WEBHOOK_HOST
    log.info(f"Webhook URL being set: {WEBHOOK_URL}")  # Added logging for WEBHOOK_URL
    await bot.set_webhook(url=WEBHOOK_URL)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url == WEBHOOK_URL:
        log.info("Webhook set successfully!")
    else:
        log.error(f"Webhook was not set correctly. Current URL: {webhook_info.url}")
    print(f"Webhook set to: {WEBHOOK_URL}")

async def on_shutdown(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    print("Webhook deleted.")

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    app = web.Application()
    webhook_requests_handler = web.middleware(setup_webhook(
        dispatcher=dp,
        bot=bot,
    ))
    app.add_routes([web.post(WEBHOOK_PATH, webhook_requests_handler)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()
    print(f"Webhook app started on http://{WEBAPP_HOST}:{WEBAPP_PORT}{WEBHOOK_PATH}")

    # Keep the server running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Webhook app stopped.")