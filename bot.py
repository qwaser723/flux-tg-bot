import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import os
from aiohttp import web

TOKEN = "7915198856:AAG3FE3kttx7LHZINz_BDHSAwFOj5ZGep5U"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ←←← САМЫЙ СТАБИЛЬНЫЙ FLUX-API НОЯБРЬ 2025
API_URL = "https://api.tiro.ai/v1/flux/schnell"

async def generate_image(prompt: str):
    payload = {
        "prompt": prompt,
        "width": 1024,
        "height": 1024,
        "steps": 20
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["images"][0]["url"]
    return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "FluxArt ULTRA 2025\n\n"
        "Пиши любой промт — получай HD-картинку за 6–12 сек!\n\n"
        "Примеры:\n• киберпанк девушка\n• кот в космосе\n• реалистичный дракон"
    )

@dp.message()
async def generate(message: Message):
    await message.answer("Генерирую… 🔥")
    url = await generate_image(message.text)
    if url:
        await message.answer_photo(url, caption=f"Готово за секунды!\n\n{message.text}")
    else:
        await message.answer("Сервер перегружен, жду 5 сек и попробую ещё раз…")
        await asyncio.sleep(5)
        url = await generate_image(message.text)
        if url:
            await message.answer_photo(url, caption=f"Готово!\n\n{message.text}")
        else:
            await message.answer("Сервер временно занят, попробуй через минуту")

# ←←← ДЕРЖИМ RENDEЖ ЖИВЫМ (обязательно)
async def web_handler(request):
    return web.Response(text="Flux бот живой!")

app = web.Application()
app.router.add_get('/', web_handler)

async def main():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
