from vk.api import VKAPI
from vk.bot.updater import Updater
from vk.bot.handlers import CommandHandler
import constants.vk
import asyncio
import logging
from bot.commands import commands
import json
import utils
import strings
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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
        logging.info('Запуск поллинга...')
        await updater.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(keyboard_checker())
    loop.create_task(main())
    loop.run_forever()
