# main.py
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from keys import BOT_TOKEN
from bot import router

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
dp.include_router(router)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("✅ Бот запущен!\n\nПопробуй команду /help.")

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "Доступные команды:\n"
        " /start — старт\n"
        " /help  — подсказка\n"
        " просто напиши любое сообщение — получишь echo."
    )

@dp.message()
async def echo(message: types.Message):
    await message.answer(f"Ты написал: {message.text}")

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

