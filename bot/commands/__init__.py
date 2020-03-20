from . import *
import os
from importlib import import_module
from vk.bot.handlers import CommandHandler
import logging
commands = list()


class Attrs:
    def __init__(self, module):
        self.module = module

    def get(self, attr):
        try:
            return getattr(self.module, attr)
        except AttributeError:
            return None


def load():
    dirpath = os.path.dirname(__file__)
    for path in os.listdir(dirpath):
        # Тянем все файлы, кроме __init__.py
        if not path.startswith('__'):
            imported_module = import_module('.' + path[:-3], package=__name__)
            attrs = Attrs(imported_module)
            # Получаем объекты из файлов в папке с командами.
            command_text = attrs.get('text')
            command_func = attrs.get('command')
            entry_point = attrs.get('entry_point')
            fallback = attrs.get('fallback')

            # Если это обыная команда
            if command_func:
                logging.info(f'Добавлена команда "{command_text}"')
                commands.append(CommandHandler(command_text, command_func))
            # # Если это команда с диалогом (когда нужно ввести какоие-то параметры)
            # elif entry_point:
            #     command_states = attrs.get('states')
            #     entry_points.append(CommandHandler(command_text, entry_point))
            #     states.update(command_states)
            # # Если это команда для прекращения диалога
            # if fallback:
            #     fallbacks.append(CommandHandler(command_text, fallback))


load()