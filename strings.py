strings = {}


def load():
    strings_file = open('data/strings.txt', 'r', encoding='utf8').read()
    for pair in strings_file.split('----'):
        if pair:
            pair = pair.split('\n', 1)
            strings[pair[0]] = pair[1]


def get(key):
    return strings.get(key, key)
