import json


def get_key():
    with open("secrets.json") as file:
        content = json.load(file)

    key = content["key"]

    return key
