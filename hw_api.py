"""
This module works with HW API and other requests related to HW (i.e. distribution results of battle)
Don't forget to check settings and url's
Remember that all requests will take some time, so VK may send another request.
You can use threads to call this functions
(c) Misden a.k.a. 1nfernos, 2021
"""
import requests

from db.squads import get_token, get_squads
from settings import fraction, debug

url = "https://aegis.hackerwars.ru/set_target"
params = {"key": "466F2FFC", "source": "", "token": "", "target": 0}

url_dist = 'https://broadcast.vkforms.ru/api/v2/broadcast?token=api_83877_pI44cDqGF88EyHn2hf5OZhnn'
params_dist = {'message': {'message': 'lol'}, 'list_ids': 762486, 'run_now': 1}


def set_target(name, target):
    params["source"] = name
    params["target"] = target
    params["token"] = get_token(name)

    if debug:
        print("request to " + url + " with " + str(params))
    else:
        requests.get(url, params)
    return


def check(name, token):
    params["source"] = name
    params["target"] = fraction
    params["token"] = token
    print("request to " + url + " with " + str(params))

    if debug:
        return True
    else:
        r = requests.get(url, params)
        return 'Attack on yourself forbidden.' in str(r.content)


def distribute(msg="test"):
    params_dist['message']['message'] = msg

    if debug:
        print("request to " + url_dist + " with " + str(params_dist))
    else:
        requests.post(url_dist, json=params_dist)
    return


def remove_all():
    # !!!It takes too long, VK send second request
    for src in get_squads():
        params["source"] = src
        params["target"] = 0
        params["token"] = get_token(src)

        if debug:
            print("request to " + url + " with " + str(params))
        else:
            requests.get(url, params)

    return
