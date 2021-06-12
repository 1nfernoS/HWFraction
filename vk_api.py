"""
This module works with VK API.
There is not much def-s, but you can add any method from https://vk.com/dev/callback_api
(c) Misden a.k.a. 1nfernos, 2021
"""
from settings import token, debug, errors_chat
import json
import vk

api = vk.API(vk.Session(), v='5.126')


def error(msg):
    """
    Log error to error chat
    :param msg: str, message with error
    :return: None
    """
    if debug:
        print("\n!!! Error occurred !!!\n\n"+str(msg))
    else:
        api.messages.send(access_token=token,
                          peer_id=str(errors_chat),
                          random_id=0,
                          message=str(msg))
    return


def send(chat_id, msg, kbd=None):
    """
    Send message from name of bot
    :param chat_id: int/str, id of chat to send
    :param msg: str, message to send
    :param kbd: None / dict, keyboard
    """
    if debug:
        if kbd:
            print(str(chat_id) + ':\n' + str(msg) + ',\n kbd: True')
        else:
            print(str(chat_id) + ':\n' + str(msg))
        return
    if kbd:
        api.messages.send(access_token=token,
                          peer_id=str(chat_id),
                          random_id=0,
                          message=str(msg),
                          keyboard=json.dumps(kbd),
                          disable_mentions=True,
                          dont_parse_links=True
                          )
    else:
        api.messages.send(access_token=token,
                          peer_id=str(chat_id),
                          random_id=0,
                          message=str(msg),
                          disable_mentions=True,
                          dont_parse_links=True
                          )
    return
