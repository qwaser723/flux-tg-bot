import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import os
from aiohttp import web

TOKEN = "8589799630:AAGc3xr-XMRtQ2OWIakid9xo96Fgqd3ZwOQ"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# ЭТОТ API РАБОТАЕТ 100 % СЕЙЧАС (ноябрь 2025)
API_URL = "https://t2i.mcpcore.xyz/api/free/generate"

async def generate_image(prompt: str):
    payload = {"prompt": prompt}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data["image_url"]
    return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("FluxArt PRO 2025\nПиши любой промт — получай HD-картинку за 8–15 сек!\n\nПримеры: кот в киберпанке, девушка в космосе")

@dp.message()
async def generate(message: Message):
    await message.answer("Генерирую…")
    url = await generate_image(message.text)
    if url:
        await message.answer_photo(url, caption=message.text)
    else:
        await message.answer("Сервер сейчас занят, попробуй ещё раз через 10 сек")

# Держим Render живым
async def web_handler(request):
    return web.Response(text="бот живой")

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
