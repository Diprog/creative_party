import logging

strings_path = 'data/strings.txt'
strings = {}


def load():
    logging.info(f'Открытие файла со строками {strings_path}')
    strings_file = open(strings_path, 'r', encoding='utf8').read()
    for pair in strings_file.split('----'):
        if pair:
            pair = pair.split('\n', 1)
            strings[pair[0]] = pair[1]
            logging.info(f'{pair[0]} - Загружено')


def get(key):
    return strings.get(key, key)
