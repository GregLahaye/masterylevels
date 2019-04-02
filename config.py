import json


def get_value(key):
    with open("config.json") as file:
        content = json.load(file)

    if key in content.keys():
        value = content[key]
    else:
        print("{} does not exist".format(key))
        value = None

    return value
