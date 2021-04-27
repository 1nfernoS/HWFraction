"""
This module handles all payload data. I don't sure how it will be in the end, but now we have description ^^
(c) Misden a.k.a. 1nfernoS, 2021
"""
import vk_api
from hw_api import set_target
from settings import fraction

import db.users as users


def start(msg, payload):
    # TODO: make normal payloads, not only target parse
    chat = msg['peer_id']
    user_id = msg['from_id']
    role_id = users.get_role(user_id)
    target(msg=msg, payload=payload, chat=chat, role_id=role_id)
    return


def target(**kwargs):
    roles = [0, 1, 3, 5, 7]
    # TODO
    # in multiThreading

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        set_target(str(fraction), kwargs['payload']['target'])

    # Squad Leader
    else:
        source = users.get_squad(kwargs['msg']['from_id'])
        set_target(source, kwargs['payload']['target'])

    vk_api.send(kwargs['chat'], "target sent!")
    return
