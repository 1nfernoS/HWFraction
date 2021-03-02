import requests
from settings import squad_list

url = "https://aegis.hackerwars.ru/set_target"
params = {"key": "466F2FFC", "source": "", "token": "", "target": 0}


def set_target(name, target):
    params["source"] = name
    params["target"] = target
    params["token"] = squad_list[name]
    requests.get(url, params)
    return None


def check(name, token):
    params["source"] = name
    params["target"] = 3
    params["token"] = token
    r = requests.get(url, params)
    return 'Attack on yourself forbidden.' in str(r.content)


def remove_all():
    # !!!It takes too long, VK send second request
    for src in squad_list:
        params["source"] = src
        params["target"] = 0
        params["token"] = squad_list[src]
        requests.get(url, params)
    return None
