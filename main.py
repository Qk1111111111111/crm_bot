import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from keys import BOT_TOKEN
from bot import router

bot_client = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("бот работает")

async def main():
    print("BOT STARTED")
    await dp.start_polling(bot_client)

if __name__ == "__main__":
    asyncio.run(main())