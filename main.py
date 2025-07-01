import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types.error_event import ErrorEvent
from data.models import async_main
from apps import handlers, callbacks
from secret.config import TOKEN, BOT_PROPERTIES
from log.antispam import AntiFloodMiddleware
from log.check_subscribe import CheckSubscribtion
from log.logging import start_logging, log

bot = Bot(token=TOKEN, default=BOT_PROPERTIES)
dp = Dispatcher()


@dp.error()
async def global_error_handler(event: ErrorEvent) -> None:
    log.error(f"{event.exception}", exc_info=True)


async def main():
    await async_main()
    await start_logging()

    dp.message.middleware(AntiFloodMiddleware())
    dp.message.middleware(CheckSubscribtion())
    dp.include_routers(handlers.router, callbacks.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot is sleep")
