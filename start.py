import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

import asyncio

import constants.vk
from bot.commands import commands
from vk.api import VKAPI
from vk.bot.updater import Updater
from vk.bot.handlers import WallHandler
import strings
import db.posts


async def wall_handler(vk, update):
    print(update['object'])


async def keyboard_checker():
    while True:
        await asyncio.sleep(0)


async def main():
    async with VKAPI([constants.vk.GROUP_TOKEN]) as vk:
        updater = Updater(vk, constants.vk.GROUP_ID)

        dispatcher = updater.dispatcher
        logging.info('Загрузка команд...')
        for command in commands:
            dispatcher.add_handler(command)
        dispatcher.add_handler(WallHandler(wall_handler))

        logging.info('Запуск поллинга...')
        await updater.start_polling()


if __name__ == '__main__':
    strings.load()
    loop = asyncio.get_event_loop()
    loop.create_task(keyboard_checker())
    loop.create_task(main())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logging.info('Остановка программы...')
