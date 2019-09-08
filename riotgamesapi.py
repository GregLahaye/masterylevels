import config
import secrets
import requests
import json


def account(region, summoner):
    region = region.upper()
    if region in REGIONS:
        key = secrets.get_key()

        base_url = BASE_API.format(region=region)
        summoner_url = SUMMONER_API.format(summoner=summoner, key=key)

        r = requests.get(base_url + summoner_url)
        if r.status_code == 200:
            content = {"success": True, "response": r.json()}

        else:
            content = {"success": False, "response": r.text}

    else:
        content = {"success": False, "response": "invalid region"}

    return content


def masteries(region, summoner_id):
    key = secrets.get_key()

    base_url = BASE_API.format(region=region)
    mastery_url = MASTERY_API.format(summoner_id=summoner_id, key=key)

    r = requests.get(base_url + mastery_url)
    if r.status_code == 200:
        content = {"success": True, "response": r.json()}

    else:
        content = {"success": False, "response": r.text}

    return content


def parse(masteries):
    champions = []
    for champion in masteries:
        champion_id = champion["championId"]
        champion_name = id_to_name(champion_id)

        version = config.get_value("version")["champion"]
        image_url = IMAGE_API.format(version=version, champion_name=champion_name)

        chest_granted = champion["chestGranted"]

        champion_level = champion["championLevel"]
        if champion_level == 5:
            tokens = champion["tokensEarned"]
            level_progress = (tokens / 3) * 100
        elif champion_level == 6:
            tokens = champion["tokensEarned"]
            level_progress = (tokens / 3) * 100
        elif champion_level == 7:
            level_progress = 100
        else:
            xp_since = champion["championPointsSinceLastLevel"]
            xp_until = champion["championPointsUntilNextLevel"]
            level_progress = (xp_since / (xp_since + xp_until)) * 100

        info = [champion_name, champion_level, level_progress, chest_granted, image_url]
        champions.append(info)

    # sort champions based on level, progress, chest, name
    champions = sorted(champions, key=lambda champions:(champions[1],
        champions[2], champions[3], champions[0]), reverse=True)
    
    return champions


def id_to_name(champion_id):
    with open("champion.json") as file:
        content = json.load(file)

    champions = content["data"]
    for champion in champions.values():
        if int(champion["key"]) == int(champion_id):
            champion_name = champion["id"]
            return champion_name


BASE_API = "https://{region}.api.riotgames.com"
SUMMONER_API = "/lol/summoner/v4/summoners/by-name/{summoner}?api_key={key}"
MASTERY_API = "/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={key}"
IMAGE_API = (
    "https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{champion_name}.png"
)
REGIONS = [
    "BR1",
    "EUN1",
    "EUW1",
    "JP1",
    "KR",
    "LA1",
    "LA2",
    "NA",
    "NA1",
    "OC1",
    "TR1",
    "RU",
]
