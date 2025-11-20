import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import json
from flask import Flask
import os

TOKEN = "8580070471:AAGujcp6UwmaBNES6S01buVr8TzHFFF6cu4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

API_URL = "https://t2i.mcpcore.xyz/api/free/generate"

async def generate_image(prompt, model="turbo"):
    data = {"prompt": prompt, "model": model}
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
                        if event.get("status") == "error":
                            return None
                    except: pass
    return None

@dp.message()
async def any_message(m: Message):
    if m.text == '/start':
        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(InlineKeyboardButton("Turbo", callback_data="turbo"), InlineKeyboardButton("Flux", callback_data="flux"))
        await m.answer(
            "FluxArt PRO v4.0 — генерирую HD-картинки по промту за 8–15 сек!\n\n"
            "Выбери модель или пиши промт прямо сейчас.\nПример: 'кот в космосе киберпанк'",
            reply_markup=kb
        )
    else:
        await m.answer("Генерирую… (8–15 сек)")
        image_url = await generate_image(m.text, "turbo")
        if image_url:
            await m.answer_photo(image_url, caption=f"Твоя картинка по '{m.text}'! (Turbo модель)")
        else:
            await m.answer("Ошибка генерации, попробуй другой промт")

async def main():
    await dp.start_polling(bot)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot alive!"

if __name__ == '__main__':
    from threading import Thread
    Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': int(os.environ.get("PORT", 8080))}).start()
    asyncio.run(main())
