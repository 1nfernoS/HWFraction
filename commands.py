"""
This module handles all commands (messages without payload and starting with '/' or other prefix.
All commands should have single def and have same name like prefix-command (i.e. /ping calls def 'ping').
For saving structure, call 'start' method with command name. If you want, you can refactor it into class.
Add new def-s after 'cmd_list'. This will keep 'cmd_list' work properly
If you want to expand imports, don't forget to increase cmd_list's globals start value by count of new imports.
You can not following this recommendations, but in this case you all doing at your owh risk
(c) Misden a.k.a. 1nfernoS, 2021
"""
import copy

import vk_api
import hw_api
import kbd_list
from settings import fraction, start_time, ignored_squads

import db.users as users
import db.squads as squads
from db.db_sql import query


def start(msg, command):
    chat = msg['peer_id']
    user_id = msg['from_id']
    user = users.get_user(user_id)
    globals()[command](msg=msg, chat=chat, user=user)
    return


def cmd(**kwargs):
    """
    List of all commands here
    :return: list [ %command_name%: str ]
    """
    return list(globals())[20:]


def cmd_list(**kwargs):
    """
    Send in vk list of commands
    """
    roles = [0]
    user = kwargs['user']

    if user['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    com_list = cmd()
    msg = 'There are ' + str(len(com_list)) + ' commands:\n'
    msg += '\n'.join(com_list)
    vk_api.send(kwargs['chat'], msg)
    return


def user(**kwargs):
    """
    Send in vk list of squad's user or list of leaders (associates and leaders)
    """
    roles = [0, 1, 3, 5, 7]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        com = kwargs['msg']['text'].split()
        if len(com) == 2:
            com[1] = com[1].upper()
            if com[1] not in squads.get_squads():
                vk_api.send(kwargs['chat'], "Wrong squad")
                return
            squad_users = squads.squad_users(com[1])
            msg = ''
            for i in squad_users:
                msg = msg + '[id' + str(i) + '|' + str(squad_users[i]) + ']\n'
            if msg == '':
                vk_api.send(kwargs['chat'], "Empty...")
            else:
                vk_api.send(kwargs['chat'], msg)
            return
        elif len(com) == 1:
            leaders = list()
            for squad in squads.get_squads():
                for lead in squads.get_leaders(squad):
                    leaders.append(lead)
            msg = ''
            for i in leaders:
                msg = msg + '[id' + str(i) + '|' + users.get_profile(i)['nickname'] + ']: ' + str(users.get_role(i)) + '\n'
            if msg == '':
                vk_api.send(kwargs['chat'], "Empty...")
            else:
                vk_api.send(kwargs['chat'], msg)
            return
        else:
            # TODO
            vk_api.send(kwargs['chat'], "Wrong arguments, (source) is needed")
    # SquadLeader
    else:
        squad_users = squads.squad_users(users.get_squad(kwargs['msg']['from_id']))
        msg = ''
        for i in squad_users:
            msg = msg + '[id' + str(i) + '|' + str(squad_users[i]) + ']\n'
        if msg == '':
            vk_api.send(kwargs['chat'], "Empty...")
        else:
            vk_api.send(kwargs['chat'], msg)
    return


def role(**kwargs):
    """
    Apply new role to user by reply or forward
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    command = kwargs['msg']['text'].split()
    if len(command) != 2:
        vk_api.send(kwargs['chat'], "Wrong arguments, role id needed")
        return
    if 'reply_message' in kwargs['msg'].keys():
        user_id = kwargs['msg']['reply_message']['from_id']
    else:
        if len(kwargs['msg']['fwd_messages']) == 1:
            user_id = kwargs['msg']['fwd_messages'][0]['from_id']
        else:
            vk_api.send(kwargs['chat'], "No reply or wrong forward")
            return

    if user_id < 0:
        vk_api.send(kwargs['chat'], "Only users can have roles")
        return

    squads_count = squads.count_squads()-1
    '''
    1 Creator, 1 TeamLeader, up to 5 other TeamLeaders
    SquadLeaders = count squads without fraction, 
    up to 20 Squad members per squad, including leader
    '''
    role_limit = {0: 1, 1: 1, 2: 5, 5: squads_count, 9: squads_count*19}

    role_id = int(command[1])
    if role_id < 0 or role_id > 13:
        vk_api.send(kwargs['chat'], "Wrong role id")
        return
    try:
        limit = users.count_role(role_id) < role_limit[role_id]
    except KeyError:
        limit = True
    if limit:
        users.set_role(user_id, role_id)
        vk_api.send(kwargs['chat'], "Role set!")
    else:
        vk_api.send(kwargs['chat'], "Limit of Role!")
    return


def role_list(**kwargs):
    """
    Send in vk list of all roles
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    r_list = users.get_roles()
    message = ''
    for i in r_list:
        message = message + i + '\n'
    vk_api.send(kwargs['msg']['from_id'], message)
    vk_api.send(kwargs['chat'], "List sent in your chat")
    return


def ping(**kwargs):
    """
    Send in vk message that bot is working
    """
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    vk_api.send(kwargs['chat'], "Still Alive from " + str(int(start_time)))
    return


def test(**kwargs):
    """
    Ummmm... Nothing... Really
    """
    vk_api.send(kwargs['chat'], kwargs['msg'])
    return


def delete(**kwargs):
    """
    Delete user and register him by forward or reply
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    if 'reply_message' in kwargs['msg'].keys():
        user_id = kwargs['msg']['reply_message']['from_id']
    else:
        if len(kwargs['msg']['fwd_messages']) == 1:
            user_id = kwargs['msg']['fwd_messages'][0]['from_id']
        else:
            vk_api.send(kwargs['chat'], "No reply or wrong forward")
            return

    if user_id < 0:
        vk_api.send(kwargs['chat'], "Only users can have roles")
        return

    users.del_user(user_id)
    users.reg_user(user_id, kwargs['msg']['date'])

    return


def kill(**kwargs):
    """
    Raises Exception to kill bot. Used to check stability and error logging
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    raise Exception


def kbda(**kwargs):
    """
    Set target 0 for all squads
    [WARNING] Long requests, can works double
    """
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return
    hw_api.remove_all()
    vk_api.send(kwargs['chat'], "Keyboards are removed")
    return


def id(**kwargs):
    """
    Send in vk id of user if reply or forward? else send chat id
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    if 'reply_message' in kwargs['msg'].keys():
        vk_api.send(kwargs['chat'], kwargs['msg']['reply_message']['from_id'])
        return
    elif len(kwargs['msg']['fwd_messages']) == 1:
        vk_api.send(kwargs['chat'], kwargs['msg']['fwd_messages'][0]['from_id'])
        return
    else:
        vk_api.send(kwargs['chat'], kwargs['msg']['peer_id'])
        return


def kbd(**kwargs):
    """
    Send in vk keyboard for setting targets
    """
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    if kwargs['chat'] < 2000000000:
        vk_api.send(kwargs['chat'], "This is not conversation!")
        return

    # We need to modify keyboard without affecting to original
    keyboard = copy.deepcopy(kbd_list.target)
    keyboard['buttons'].pop()
    vk_api.send(kwargs['chat'], "Your keyboard!", keyboard)
    return


def kbdd(**kwargs):
    """
    Send in vk empty keyboard
    """
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    if kwargs['chat'] < 2000000000:
        vk_api.send(kwargs['chat'], "This is not conversation!")
        return

    keyboard = {'one_time': True, 'buttons': []}
    # We need to modify keyboard without affecting to original
    vk_api.send(kwargs['chat'], "Keyboard removed!", keyboard)
    return


def reg_squad(**kwargs):
    """
    Add new squad with source and token
    """
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    com = kwargs['msg']['text'].split()

    if len(com) != 3:
        vk_api.send(kwargs['chat'], "Wrong arguments, squad and token needed")
        return

    if len(com[1]) > 2:
        vk_api.send(kwargs['chat'], "Use initials of squad (xx) for squad name")
        return
    com[1] = com[1].upper()

    if len(com[2]) != 128 or not hw_api.check(com[1], com[2]):
        vk_api.send(kwargs['chat'], "Wrong token or squad")
        return
    else:
        squads.reg_squad(com[1], com[2])
        vk_api.send(kwargs['chat'], "Squad registered successfully")
    return


def target(**kwargs):
    """
    Send target to HW API
    """
    roles = [0, 1, 3, 5, 7]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    com = kwargs['msg']['text'].split()

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        if len(com) == 3:

            try:
                com[2] = int(com[2])
            except ValueError:
                vk_api.send(kwargs['chat'], "Wrong target, should be number")
                return

            if 0 <= com[2] <= 7:
                if com[2] == fraction:
                    vk_api.send(kwargs['chat'], 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(kwargs['chat'], 'Wrong target')
                return

            if com[1] != 'all':
                com[1] = com[1].upper()
                if com[1] not in squads.get_squads():
                    vk_api.send(kwargs['chat'], "Wrong source")
                    return
                if com[1] in ignored_squads:
                    vk_api.send(kwargs['chat'], "Dead squad")
                    return

                hw_api.set_target(com[1], com[2])
            else:
                for source in squads.get_squads():
                    if source in ignored_squads:
                        pass
                    else:
                        hw_api.set_target(source, com[2])
            vk_api.send(kwargs['chat'], "Target sent!")
            return

        elif len(com) == 2:

            try:
                com[1] = int(com[1])
            except ValueError:
                vk_api.send(kwargs['chat'], "Wrong target, should be number")
                return

            if 0 <= com[1] <= 7:
                if com[1] == fraction:
                    vk_api.send(kwargs['chat'], 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(kwargs['chat'], 'Wrong target')
                return

            hw_api.set_target(str(fraction), com[1])
            vk_api.send(kwargs['chat'], "target sent!")
            return

        else:
            vk_api.send(kwargs['chat'], "Wrong arguments, (source and) target needed")
            return

    # Squad Leader
    else:
        if len(com) != 2:
            vk_api.send(kwargs['chat'], "Wrong arguments, target needed")
            return

        try:
            com[1] = int(com[1])
        except ValueError:
            vk_api.send(kwargs['chat'], "Wrong target, should be number")
            return

        if 0 <= com[1] <= 7:
            if com[1] == fraction:
                vk_api.send(kwargs['chat'], 'Attack on yourself')
                return
        else:
            # target = -1 or 9
            vk_api.send(kwargs['chat'], 'Wrong target')
            return

        source = users.get_squad(kwargs['msg']['from_id'])
        hw_api.set_target(source, com[1])
        vk_api.send(kwargs['chat'], "target sent!")
        return


def squad_list(**kwargs):
    """
    Send in vk squad list
    """
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    msg = ', '.join(squads.get_squads())

    vk_api.send(kwargs['chat'], msg)
    return


def del_squad(**kwargs):
    """
    Delete squad from DB
    """
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    com = kwargs['msg']['text'].split()
    if len(com) != 2:
        vk_api.send(kwargs['chat'], "Wrong argument, source is needed")
        return

    if com[1] not in squads.get_squads():
        vk_api.send(kwargs['chat'], "Squad already doesn't exists")
        return

    # TODO: Check for user in squad

    squads.del_squad(com[1])
    vk_api.send(kwargs['chat'], "Squad deleted")
    return


def home(**kwargs):
    """
    Return to home page if bot broke
    """
    if kwargs['chat'] > 2000000000:
        return
    kb = kbd_list.main
    vk_api.send(kwargs['chat'], "Home", kb)
    return


# TODO: Remove after tests
def db_query(**kwargs):
    """
    Execute query directly into DB and send result into chat
    !!! [DANGER] !!! Use it only if you 101% sure what are you doing
    """
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    q = kwargs['msg']['text'].replace('/query ', '')
    res = query(q)
    vk_api.send(kwargs['msg']['from_id'], res)
    vk_api.send(kwargs['chat'], "Result is in your chat")

    return
