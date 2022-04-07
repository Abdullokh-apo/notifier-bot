import asyncio

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import ParseMode

from db.db import DB
from loader import bot, dp
from parsing.main import Anime

user_id = 0
an = Anime('parsing/lastkey.txt')
db = DB('db/db.db')


@dp.message_handler(Command("start"))
async def start(msg: types.Message):
    await msg.answer('Мы будем уведомлять вас о выходе новых аниме на сайте '
                     'animego.org')
    db.add_user(msg.from_user.id)


async def scheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        new_films = an.new_films()
        if new_films:
            new_films.reverse()
            for nf in new_films:
                info = an.film_info(nf)

                users = db.get_users()
                for user in users:
                    with open(an.download_image(info['image']),
                              'rb') as img:
                        await bot.send_photo(
                            user[0],
                            img,
                            caption=f'<b>{info["title"]}</b>\n'
                                    f'<b>Жанр: </b>'
                                    f'{info["genre"]}\n\n'
                                    f'{info["description"].strip()[:600]}\n\n'
                                    f'{info["link"]}',
                            disable_notification=True
                        )

                an.update_lastkey(info['id'])
