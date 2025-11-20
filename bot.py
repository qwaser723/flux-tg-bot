import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import json
import os

TOKEN = "8580070471:AAGujcp6UwmaBNES6S01buVr8TzHFFF6cu4"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

API_URL = "https://t2i.mcpcore.xyz/api/free/generate"

async def generate_image(prompt):
    data = {"prompt": prompt, "model": "turbo"}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=data) as resp:
            if resp.status != 200: return None
            text = await resp.text()
            for line in text.split('\n'):
                if 'data: ' in line:
                    try:
                        event = json.loads(line.split('data: ')[1])
                        if event.get("status") == "complete":
                            return event.get("imageUrl")
                    except: pass
    return None

@dp.message_handler(commands=['start'])
async def start(m: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(InlineKeyboardButton("Turbo", callback_data="m_turbo"))
    await m.answer("FluxArt PRO 2025\nПиши промт — получишь Flux-картинку за 8 сек!", reply_markup=kb)

@dp.message_handler()
async def any_text(m: types.Message):
    await m.answer("Генерирую…")
    url = await generate_image(m.text)
    if url:
        await m.answer_photo(url, caption=f"Готово! 🔥\n{m.text}")
    else:
        await m.answer("Ошибка, попробуй другой промт")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
