"""
This module handles all payload data. All payloads have types, so you can check it in schema.json (later)
(c) Misden a.k.a. 1nfernoS, 2021
"""
import copy

import vk_api
from hw_api import set_target
from settings import fraction, fractions
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
    """
    Send in vk new keyboard
    """
    pl = kwargs['payload']
    kbd = keyboard(pl, kwargs['role_id'], kwargs['msg']['from_id'])
    # kbd = getattr(kbd_list, pl)
    # TODO: +-Edit kbd if role
    # TODO: +-Make page titles (Battle_Push page looks not safe)
    msg = kwargs.get('flag', page_text(pl, kwargs['msg']))
    vk_api.send(kwargs['chat'], msg, kbd)
    return


def page_text(name, message):
    """
    Generating texts for pages
    :param name: str, name of page
    :param message: dict, message object from vk [object][message]
    :return: text for page
    """
    if name == 'main':
        user_id = message['from_id']
        user_data = users.get_user(user_id)
        # dict {user_id: int, role: int,
        #     subscribe: bool, report: bool, show_profile: bool, show_report: bool,
        #     nickname: str, squad: str, practice: int, theory: int, guile: int, wisdom: int;
        #     if report True: date_report: str, income: int, pure_income: int, target: int}
        text = 'Hello, ' + user_data['nickname'] + '\n\n'
        if user_data['show_profile']:
            # stat's string
            text += '&#128225;: ' + str(user_data['practice']) + '; &#128190;: ' + str(user_data['theory']) + \
                    '; &#128241;: ' + str(user_data['guile']) + '; &#128270;: ' + str(user_data['wisdom']) + '\n'
            # overall string
            text += '&#9876;: ' + str(int(user_data['practice'] + 1.5*user_data['guile'])) + \
                    '; &#128272;: ' + str(int(user_data['theory'] + 1.5*user_data['wisdom'])) + '\n\n'
        if user_data['show_report']:
            if user_data['report']:
                text += '&#129297;: ' + str(user_data['income']) + '; &#128181;: ' + str(user_data['pure_income']) +\
                        '; &#9989;: ' + str(fractions[user_data['target']]) + '\n\n'
            else:
                text += 'Today you don\'t send report\n\n'
        # TODO: get time before battle
        text += 'Time left for battle: ' + str('undefined')
        return text
    elif name == 'settings':
        text = 'Settings page'
        return text
    elif name == 'stats':
        # TODO: Remove brackets after complete stats
        text = 'Statistics.\nHere you can watch your performance (not working)'
        return text
    elif name == 'control':
        text = 'Control page.\nAll for your business'
        return text
    elif name == 'battle_push':
        text = 'Manage pushes for battle'
        return text
    elif name == 'target':
        user_id = message['from_id']
        role_id = users.get_role(user_id)
        text = 'Set target for ' + ('fraction' if role_id in [0, 1, 3] else users.get_squad(user_id))
        return text
    else:
        pass
    return


def keyboard(kb, role, user):
    """
    Configure keyboard for user's role
    :param kb: dict, original keyboard page
    :param role: int
    :param user: int, user id from vk [from_id]
    :return: dict, configured keyboard
    """
    orig_kbd = getattr(kbd_list, kb)
    kbd = copy.deepcopy(orig_kbd)
    # TODO: Role lists for flags (not sure is need or not)
    if kb == 'main':
        if role in [0, 1, 3, 5, 7]:
            pass
        else:
            # Hide control page
            kbd['buttons'].pop()
    elif kb == 'settings':
        u = users.get_preferences(user)
        subscribe = u['subscribe']
        show_profile = u['show_profile']
        show_report = u['show_report']
        prefs = kbd['buttons'][0]

        if show_report:
            prefs[0]['color'] = 'positive'
            prefs[0]['action']['label'] = 'Hide Report'
        else:
            prefs[0]['color'] = 'negative'
            prefs[0]['action']['label'] = 'Show Report'

        if show_profile:
            prefs[1]['color'] = 'positive'
            prefs[1]['action']['label'] = 'Hide Profile'
        else:
            prefs[1]['color'] = 'negative'
            prefs[1]['action']['label'] = 'Show Profile'

        if subscribe:
            prefs[2]['color'] = 'positive'
            prefs[2]['action']['label'] = 'Unsubscribe'
        else:
            prefs[2]['color'] = 'negative'
            prefs[2]['action']['label'] = 'Subscribe'

        if role in [0, 1, 3, 5, 7]:
            pass
        else:
            # Hide push page
            kbd['buttons'].pop(1)
    elif kb == 'stats':
        if role in [0, 1, 3, 5, 7, 9]:
            pass
        else:
            # Hide squad stats
            kbd['buttons'].pop(1)
        pass
    elif kb == 'control':
        if role in [3, 7]:
            # Hide notes and manage list
            kbd['buttons'].pop(1)
    elif kb == 'battle_push':
        """
        if role in [0, 1, 3]:
            # TODO: Squad kbd
            kbd['buttons'].pop(0)
            kbd['buttons'].pop(0)
        else:
            pass
        """
        pass
    else:
        pass
    return kbd


def toggle(**kwargs):
    """
    Change preference or battle push
    """
    preference = kwargs['payload']
    if preference != 'push':
        users.change_preference(kwargs['chat'], preference)
        msg = 'You have successfully changed preference'
        page(msg=kwargs['msg'], payload='settings', chat=kwargs['chat'], role_id=kwargs['role_id'], flag=msg)
    else:
        # TODO: Push toggle
        blocked(kwargs['chat'])
    return


def target(**kwargs):
    """
    Set target buttons
    """
    roles = [0, 1, 3, 5, 7]
    # TODO: in multiThreading (or somehow after request)

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
    """
    Get statistics for type
    """
    # TODO: Generating stats (list or graphics)
    blocked(kwargs['chat'])
    return


def inputs(**kwargs):
    """
    Pre-process raw input
    """
    # TODO: Make inputs are possible (and check for injections)
    blocked(kwargs['chat'])
    return


def item(**kwargs):
    """
    Get data example for lists
    """
    # TODO: Make generator for keyboard
    blocked(kwargs['chat'])
    return


def lists(**kwargs):
    """
    Generated keyboards for user
    """
    # TODO: Make generator for lists
    blocked(kwargs['chat'])
    return


def blocked(chat):
    """
    Just for keep bot safe
    :param chat: int, [peer_id]
    :return: None
    """
    vk_api.send(chat, "This function is temporary unavailable")
    return
