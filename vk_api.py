import vk
import random
from settings import *
import json

api = vk.API(vk.Session(), v='5.126')


def send(user_id, msg, kbd=None):
    if kbd:
        api.messages.send(access_token=token,
                          peer_id=str(user_id),
                          random_id=random.getrandbits(64),
                          message=str(msg),
                          keyboard=json.dumps(kbd)
                          )
    else:
        api.messages.send(access_token=token,
                          peer_id=str(user_id),
                          random_id=random.getrandbits(64),
                          message=str(msg)
                          )
    return None
