import json
import logging
import asyncio
import os
import content
import parse as parse

from aiogram import Bot, Dispatcher, executor, types

import keyboards as kb




logging.getLogger("pika").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)



token = os.environ['TELEGRAM_API_TOKEN']
ids = os.environ['TG_IDS']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer(content.start_text)
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    consumers = ids.split()
    logging.info(f'consumers: {consumers}')

    loop.create_task(parse.broadcast(bot, consumers))
    executor.start_polling(dp, skip_updates=True)
