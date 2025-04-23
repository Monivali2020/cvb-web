# CVB/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# === TELEGRAM BOT ===
BOT_TOKEN    = os.getenv("CVB_TELE_API")
API_ID       = os.getenv("API_ID")
API_HASH     = os.getenv("API_HASH")

# === DATABASES ===
POSTGRES_URL      = os.getenv("POSTGRES_URL")
LOCAL_POSTGRES_URL= os.getenv("LOCAL_POSTGRES_URL")
MONGO_URL         = os.getenv("MONGO_URL")
SQLITE_URL        = os.getenv("SQLITE_URL")

# === CHARTS & COINGECKO ===
COINGECKO_API      = os.getenv("COINGECKO_API")
QUICKCHART_BASE_URL= os.getenv("QUICKCHART_BASE_URL")
CHART_THEME        = os.getenv("CHART_THEME", "dark")

# === PAYMENTS ===
NOWPAYMENTS_API_KEY = os.getenv("CVBNPAPI")
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
FLW_SECRET_KEY      = os.getenv("FLUTTERWAVE_SECRET_KEY")

# === AI ===
GEMINI_API_KEY      = os.getenv("CVB_GAPI")
OPENROUTER_API_KEY  = os.getenv("CVBAI")
HUGGINGFACE_API_KEY = os.getenv("HCVBHFAI")
META_AI_API_KEY     = os.getenv("META_AI_API_KEY")

# === MISC ===
FLASK_SECRET_KEY    = os.getenv("FLASK_SECRET_KEY")
WEBHOOK_URL         = os.getenv("WEBHOOK_URL")
BASE_URL            = os.getenv("BASE_URL")
USE_CAPTCHA         = os.getenv("USE_CAPTCHA", "False") == "True"
CAPTCHA_TIMEOUT     = int(os.getenv("CAPTCHA_TIMEOUT", "60"))
ENABLE_GBAN         = os.getenv("ENABLE_GBAN", "False") == "True"
DISABLE_COMMANDS    = os.getenv("DISABLE_COMMANDS_LIST", "").split(",")
DEFAULT_LANGUAGE    = os.getenv("DEFAULT_LANGUAGE", "en")
LOG_CHANNEL_ID      = os.getenv("LOG_CHANNEL_ID")
ADMIN_IDS           = os.getenv("ADMIN_IDS", "").split(",")
CVB_PINKSALE_LINK   = os.getenv("CVB_PINKSALE_LINK")
BOT_START_TIME      = os.getenv("BOT_START_TIME")  # or set dynamically