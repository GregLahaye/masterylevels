import requests
import json


def update_config():
    r = requests.get(VERSION_URL)
    if r.status_code == 200:
        content = r.json()

        with open("config.json", "r") as file:
            config = json.load(file)

        for key in VERSION_KEYS:
            config["version"][key] = content["n"][key]

        with open("config.json", "w") as file:
            json.dump(config, file)

    else:
        pass
        # handle error


def update_champion():
    with open("config.json") as file:
        config = json.load(file)

    version = config["version"]["champion"]

    r = requests.get(DATA_URL.format(version=version, key="champion"))
    if r.status_code == 200:
        content = r.json()

        with open("champion.json", "w") as file:
            json.dump(content, file)

    else:
        pass
        # handle error


VERSION_URL = "https://ddragon.leagueoflegends.com/realms/na.json"
VERSION_KEYS = ["item", "rune", "mastery", "summoner", "champion", "profileicon"]
DATA_URL = "http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/{key}.json"

update_config()
update_champion()
