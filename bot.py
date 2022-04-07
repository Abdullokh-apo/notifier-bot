import asyncio
from handlers.notifier_handler import scheduled


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scheduled(1))
    executor.start_polling(dp, skip_updates=True)
