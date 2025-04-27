import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiohttp import web

# Enable basic logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("CVB_TELE_API")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"https://{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv("PORT", 8080))

# Initialize bot and dispatcher
bot = Bot(BOT_TOKEN)
dp = Dispatcher()

# Include your handlers router
from CVB.handlers import main_router
dp.include_router(main_router)

async def on_startup(bot: Bot, dispatcher: Dispatcher):
    global WEBHOOK_URL
    log.info(f"WEBHOOK_HOST from env: {WEBHOOK_HOST}")
    log.info(f"Webhook URL being set: {WEBHOOK_URL}")
    await bot.set_webhook(url=WEBHOOK_URL)
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url == WEBHOOK_URL:
        log.info("Webhook set successfully!")
    else:
        log.error(f"Webhook was not set correctly. Current URL: {webhook_info.url}")

async def webhook_handler(request: web.Request):
    token = bot.token
    if request.match_info.get("bot_token") == token:
        update = await request.json()
        from aiogram import types
        Update = types.Update.parse_obj(update)
        await dp.process_update(Update)
        return web.Response(status=200)
    else:
        return web.Response(status=403)

async def main():
    dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown) # If you have a shutdown function

    app = web.Application()
    app.add_routes([web.post(f"/bot{{bot_token}}", webhook_handler)])

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, WEBAPP_HOST, WEBAPP_PORT)
    await site.start()
    log.info(f"Webhook app started on http://{WEBAPP_HOST}:{WEBAPP_PORT}{WEBHOOK_PATH}")

    # Keep the server running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        log.info("Webhook app stopped.")