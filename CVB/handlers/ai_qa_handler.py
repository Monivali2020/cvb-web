# CVB/handlers/ai_qa.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
import aiohttp
import os

router = Router()

# Load API keys from env
GEMINI_API_KEY = os.getenv("CVB_GAPI")
OPENROUTER_API_KEY = os.getenv("CVBAI")
HUGGINGFACE_API_KEY = os.getenv("HCVBHFAI")
META_AI_API_KEY = os.getenv("META_AI_API_KEY")

@router.message(Command("ask"))
async def ai_qa_handler(message: Message):
    query = message.text.replace("/ask", "").strip()
    if not query:
        await message.reply("Please ask a question, e.g. `/ask What is Bitcoin?`", parse_mode="Markdown")
        return

    reply = await get_ai_answer(query)
    await message.reply(reply, parse_mode="Markdown")


async def get_ai_answer(query: str) -> str:
    # Priority: Gemini → OpenRouter → HuggingFace → Meta
    try:
        if GEMINI_API_KEY:
            return await ask_gemini(query)
    except:
        pass

    try:
        if OPENROUTER_API_KEY:
            return await ask_openrouter(query)
    except:
        pass

    try:
        if HUGGINGFACE_API_KEY:
            return await ask_huggingface(query)
    except:
        pass

    try:
        if META_AI_API_KEY:
            return await ask_meta(query)
    except:
        pass

    return "Sorry, all AI services are currently unavailable. Please try again later."


# AI Integrations

async def ask_gemini(prompt: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers) as resp:
            result = await resp.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]


async def ask_openrouter(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/mixtral-8x7b",  # or any other available
        "messages": [
            {"role": "system", "content": "You are a helpful crypto assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload) as resp:
            data = await resp.json()
            return data["choices"][0]["message"]["content"]


async def ask_huggingface(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api-inference.huggingface.co/models/google/flan-t5-large", headers=headers, json=payload) as resp:
            result = await resp.json()
            return result[0]["generated_text"]


async def ask_meta(prompt: str) -> str:
    headers = {"Authorization": f"Bearer {META_AI_API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "max_tokens": 200}

    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.meta.ai/generations", headers=headers, json=payload) as resp:
            result = await resp.json()
            return result["text"]