from aiogram import executor
from utils.set_bot_commands import set_default_commands
from handlers.users import dp
from loader import bot, storage


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)


async def on_shutdown(dispatcher):
    await bot.close()
    await storage.close()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=False)
