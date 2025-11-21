import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import aiohttp
import json

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# НОВЫЙ ТОКЕН УЖЕ ВСТАВЛЕН
TOKEN = "7915198856:AAG3FE3kttx7LHZINz_BDHSAwFOj5ZGep5U"
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

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
    await message.answer(
        "FluxArt PRO 2025\n\n"
        "Пиши любой промт — получай HD-картинку за 8–15 сек!\n\n"
        "Примеры:\n• кот в космосе\n• девушка в киберпанке\n• реалистичный дракон"
    )

@dp.message()
async def generate(message: Message):
    await message.answer("Генерирую…")
    url = await generate_image(message.text)
    if url:
        await message.answer_photo(url, caption=f"Готово!\n\n{message.text}")
    else:
        await message.answer("Ошибка генерации, попробуй другой промт")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
