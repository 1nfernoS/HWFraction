import requests

from db.squads import get_token, get_squads
from settings import fraction

url = "https://aegis.hackerwars.ru/set_target"
params = {"key": "466F2FFC", "source": "", "token": "", "target": 0}

url_dist = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=api_83877_pI44cDqGF88EyHn2hf5OZhnn'
params_dist = {'message': {'message': 'lol'}, 'list_ids': 762486, 'run_now': 1}


def set_target(name, target):
    params["source"] = name
    params["target"] = target
    params["token"] = get_token(name)
    # TODO: return to normal
    print("request to " + url + " with " + str(params))
    # requests.get(url, params)
    return


def check(name, token):
    params["source"] = name
    params["target"] = fraction
    params["token"] = token
    print("request to " + url + " with " + str(params))
    # TODO: return to normal
    return True
    # r = requests.get(url, params)
    # return 'Attack on yourself forbidden.' in str(r.content)


def distribute(msg="test"):
    params_dist['message']['message'] = msg
    print("request to " + url + " with " + str(params))
    # requests.post(url_dist, json=params_dist)
    return


def remove_all():
    # !!!It takes too long, VK send second request
    for src in get_squads():
        params["source"] = src
        params["target"] = 0
        params["token"] = get_token(src)
        # TODO: return to normal
        # requests.get(url, params)
        print("request to " + url + " with " + str(params))
    return
