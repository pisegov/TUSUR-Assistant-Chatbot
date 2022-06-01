import logging
import os

from aiogram import executor

import config
from utils.set_bot_commands import set_default_commands
from handlers.users import dp
from loader import bot, storage


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await bot.set_webhook(config.WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=config.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=config.WEBAPP_HOST,
        port=config.WEBAPP_PORT,
)