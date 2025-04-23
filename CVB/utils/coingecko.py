# CVB/utils/coingecko.py

import aiohttp

COINGECKO_API = "https://api.coingecko.com/api/v3"

async def get_token_price(token: str):
    url = f"{COINGECKO_API}/simple/price?ids={token}&vs_currencies=usd"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return None
            data = await response.json()
            return data.get(token, {}).get("usd")
        
# Add to CVB/utils/coingecko.py

async def get_btc_price_history(days=7):
    url = f"{COINGECKO_API}/coins/bitcoin/market_chart?vs_currency=usd&days={days}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return []
            data = await response.json()
            return data["prices"]  # [[timestamp, price], ...]
        
# CVB/utils/coingecko.py

async def get_eth_price_history(days=7):
    url = f"{COINGECKO_API}/coins/ethereum/market_chart?vs_currency=usd&days={days}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return []
            data = await response.json()
            return data["prices"]  # [[timestamp, price], ...]