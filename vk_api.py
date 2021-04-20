import vk
from settings import token, debug
import json

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
                          keyboard=json.dumps(kbd)
                          )
    else:
        api.messages.send(access_token=token,
                          peer_id=str(user_id),
                          random_id=0,
                          message=str(msg)
                          )
    return
