import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import json
import os
from aiohttp import web

TOKEN = "7915198856:AAG3FE3kttx7LHZINz_BDHSAwFOj5ZGep5U"
bot = Bot(token=TOKEN)
dp = Dispatcher()

API_URL = "https://t2i.mcpcore.xyz/api/free/generate"

async def generate_image(prompt: str):
    payload = {"prompt": prompt, "model": "turbo"}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload) as resp:
            if resp.status != 200:
                return None
            text = await resp.text()
            for line in text.splitlines():
                if line.startswith("data: "):
                    try:
                        data = json.loads(line[6:])
                        if data.get("status") == "complete":
                            return data.get("imageUrl")
                    except:
                        continue
    return None

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("FluxArt PRO 2025\nПиши промт — получай HD-картинку за 8–15 сек!\nПримеры: кот в космосе, девушка в киберпанке")

@dp.message()
async def generate(message: Message):
    await message.answer("Генерирую…")
    url = await generate_image(message.text)
    if url:
        await message.answer_photo(url, caption=f"Готово!\n\n{message.text}")
    else:
        await message.answer("Ошибка, попробуй другой промт")

# ←←← ЭТОТ КУСОК ДЕРЖИТ RENDEЖ ЖИВЫМ
async def web_handler(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.router.add_get('/', web_handler)

async def main():
    # запускаем веб-сервер на порту Render
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 8080)))
    await site.start()
    
    # запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
