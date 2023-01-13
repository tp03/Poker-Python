import json


def read_from_json(file):
    with open(file, 'r') as file_handle:
        dicts = []
        data = json.load(file_handle)
        for object in data:
            dicts.append(data[object])
        return dicts


database = read_from_json('cards_database.json')
sign = database[0]
Kicker = database[1]
