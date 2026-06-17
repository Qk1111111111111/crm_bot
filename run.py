import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

from keys import BOT_TOKEN
from app.handlers import router
import logging


print("BOT START FILE", flush=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)



bot_client = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)

logging.getLogger("aiogram").setLevel(logging.INFO)
logging.getLogger("sqlalchemy").setLevel(logging.INFO)

async def main():
    print("BOT STARTED", flush=True)

    try:
        await dp.start_polling(bot_client)
    finally:
        await bot_client.session.close()

if __name__ == "__main__":
    asyncio.run(main())