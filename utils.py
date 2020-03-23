import json


def json_dump(filepath, dictionary):
    with open(filepath, 'w', encoding='utf8') as json_file:
        json.dump(dictionary, json_file, ensure_ascii=False)


def chunks(lst, length):
    chunked = [[]]
    amount = 0
    inserted = 0
    for item in lst:
        chunked[len(chunked)-1].append(item)
        inserted += 1
        if inserted % length == 0:
            chunked.append([])
    if not chunked[-1]:
        chunked = chunked[:-1]
    return chunked