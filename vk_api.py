"""
This module works with VK API.
There is not much def-s, but you can add any method from https://vk.com/dev/callback_api
(c) Misden a.k.a. 1nfernos, 2021
"""
from settings import token, debug
import json
import vk

api = vk.API(vk.Session(), v='5.126')


def send(user_id, msg, kbd=None):
    if debug:
        if kbd:
            print(str(user_id) + ':\n' + str(msg) + ',\n kbd: True')
        else:
            print(str(user_id) + ':\n' + str(msg))
        return
    if kbd:
        api.messages.send(access_token=token,
                          peer_id=str(user_id),
                          random_id=0,
                          message=str(msg),
                          keyboard=json.dumps(kbd),
                          disable_mentions=True
                          )
    else:
        api.messages.send(access_token=token,
                          peer_id=str(user_id),
                          random_id=0,
                          message=str(msg),
                          disable_mentions=True
                          )
    return
