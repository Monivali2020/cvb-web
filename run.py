#!/usr/bin/env python3
import asyncio
from dotenv import load_dotenv

# 1. Load env
load_dotenv()

# 2. Init DB
from CVB.models.wallet_model import init_wallet_db
init_wallet_db()

# 3. Import & run your bot
from CVB.bot import main

if __name__ == "__main__":
    asyncio.run(main())