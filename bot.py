import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp
import json

TOKEN = "8580070471:AAGujcp6UwmaBNES6S01buVr8TzHFFF6cu4"
bot = Bot(token=TOKEN)
dp = Dispatcher()

API_URL = "https://t2i.mcpcore.xyz/api/free/generate"

async def generate_image(prompt):
    data = {"prompt": prompt, "model": "turbo"}
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=data) as resp:
            if resp.status != 200:
                return None
            text = await resp.text()
            for line in text.split('\n'):
                if line.startswith("data: "):
                    try:
                        js = json.loads(line[6:])
                        if js.get("status") == "complete":
                            return js.get("imageUrl")
                    except:
                        continue
    return None

@dp.message(Command("start"))
async def start(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Turbo", callback_data="model_turbo")]
    ])
    await message.answer(
        "FluxArt PRO — пиши любой промт и получай HD-картинку за 8–15 сек!\n\n"
        "Примеры:\n• девушка в киберпанке\n• кот в космосе\n• реалистичный дракон",
        reply_markup=kb
    )

@dp.message()
async def generate(message: Message):
    await message.answer("Генерирую…")
    url = await generate_image(message.text)
    if url:
        await message.answer_photo(url, caption=f"Готово за секунды!\n\n{message.text}")
    else:
        await message.answer("Ошибка генерации, попробуй другой промт")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
