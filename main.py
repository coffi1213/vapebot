import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling
from config import BOT_TOKEN
from handlers import admin, user
from utils.backup import start_backup_task

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(dispatcher)
    await start_backup_task()
    logging.info("Бот запущен.")

def register_all_handlers():
    admin.register_handlers_admin(dp)
    user.register_handlers_user(dp)

if __name__ == '__main__':
    register_all_handlers()
    start_polling(dp, skip_updates=True, on_startup=on_startup)