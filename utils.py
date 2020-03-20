import json


def json_dump(filepath, dictionary):
    with open(filepath, 'w', encoding='utf8') as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False)