# CVB/handlers/ai_qa.py

import os
import aiohttp

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

# Load your API keys from config or env
GEMINI_API_KEY      = os.getenv("CVB_GAPI")
OPENROUTER_API_KEY  = os.getenv("CVBAI")
HUGGINGFACE_API_KEY = os.getenv("HCVBHFAI")
META_AI_API_KEY     = os.getenv("META_AI_API_KEY")


@router.message(Command("ask"))
async def ai_qa_handler(message: Message):
    query = message.text.removeprefix("/ask").strip()
    if not query:
        return await message.reply(
            "Please ask a question, e.g. `/ask What is Bitcoin?`",
            parse_mode="Markdown"
        )

    reply = await get_ai_answer(query)
    await message.reply(reply, parse_mode="Markdown")


async def get_ai_answer(query: str) -> str:
    # Priority: Gemini → OpenRouter → HuggingFace → Meta
    for key, fn in (
        (GEMINI_API_KEY,     ask_gemini),
        (OPENROUTER_API_KEY, ask_openrouter),
        (HUGGINGFACE_API_KEY,ask_huggingface),
        (META_AI_API_KEY,    ask_meta),
    ):
        if key:
            try:
                return await fn(query)
            except Exception:
                continue

    return "Sorry, all AI services are unavailable. Please try again later."


async def ask_gemini(prompt: str) -> str:
    url     = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url}?key={GEMINI_API_KEY}", json=payload, headers=headers) as resp:
            result = await resp.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]


async def ask_openrouter(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type":    "application/json"
            },
            json={
                "model":    "mistralai/mixtral-8x7b",
                "messages": [
                    {"role": "system", "content": "You are a helpful crypto assistant."},
                    {"role": "user",   "content": prompt}
                ]
            }
        )
        data = await resp.json()
        return data["choices"][0]["message"]["content"]


async def ask_huggingface(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            "https://api-inference.huggingface.co/models/google/flan-t5-large",
            headers={"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"},
            json={"inputs": prompt}
        )
        result = await resp.json()
        return result[0]["generated_text"]


async def ask_meta(prompt: str) -> str:
    async with aiohttp.ClientSession() as session:
        resp = await session.post(
            "https://api.meta.ai/generations",
            headers={"Authorization": f"Bearer {META_AI_API_KEY}", "Content-Type": "application/json"},
            json={"prompt": prompt, "max_tokens": 200}
        )
        result = await resp.json()
        return result["text"]