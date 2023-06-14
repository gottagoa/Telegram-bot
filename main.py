from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


from config import TOKEN
import admin
import client
from db import create_table
import asyncio


storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)


admin.register_handlers_admin(dp)
client.register_handler_client(dp)


async def on_startup(dp: Dispatcher):
    await create_table()




if __name__ == "__main__":
    loop = asyncio.get_event_loop() 
    loop.run_until_complete(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
    