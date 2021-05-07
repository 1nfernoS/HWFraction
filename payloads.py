"""
This module handles all payload data. All payloads have types, so you can check it in schema.json (later)
(c) Misden a.k.a. 1nfernoS, 2021
"""
import vk_api
from hw_api import set_target
from settings import fraction
import kbd_list

import db.users as users


def start(msg, payload):
    chat = msg['peer_id']
    user_id = msg['from_id']
    if 'command' in payload.keys():  # first button in bot
        payload = {'type': 'page', 'value': 'main'}
    role_id = users.get_role(user_id)
    globals()[payload['type']](msg=msg, payload=payload['value'], chat=chat, role_id=role_id)
    return


def page(**kwargs):
    pl = kwargs['payload']
    kbd = getattr(kbd_list, pl)
    # TODO: Edit kbd if role
    # TODO: Make page titles (Battle_Push page looks not safe)
    vk_api.send(kwargs['chat'], pl.title() + ' page', kbd)
    return


def toggle(**kwargs):
    # TODO: Find reason why preference not changing
    vk_api.send(kwargs['chat'], "This function is temporary unavailable")
    """
    preference = kwargs['payload']
    users.change_preferences(kwargs['chat'], preference)
    msg = 'You have successfully changed preference'
    vk_api.send(kwargs['chat'], msg)
    """
    return


def target(**kwargs):
    roles = [0, 1, 3, 5, 7]
    # TODO: in multiThreading

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        set_target(str(fraction), kwargs['payload'])

    # Squad Leader
    else:
        source = users.get_squad(kwargs['msg']['from_id'])
        set_target(source, kwargs['payload'])

    vk_api.send(kwargs['chat'], "target sent!")
    return


def stats(**kwargs):
    # TODO: Generating stats
    blocked(kwargs['chat'])
    return


def inputs(**kwargs):
    # TODO: Make inputs are possible
    blocked(kwargs['chat'])
    return


def item(**kwargs):
    # TODO: Make generator for keyboard
    blocked(kwargs['chat'])
    return


def lists(**kwargs):
    # TODO: Make generator for lists
    blocked(kwargs['chat'])
    return


def blocked(chat):
    vk_api.send(chat, "This function is temporary unavailable")
    return
