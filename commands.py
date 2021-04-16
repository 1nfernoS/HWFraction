import vk_api
import hw_api
from settings import fraction

import db.users as users
import db.squads as squads


def start(msg, command):
    chat = msg['peer_id']
    user = msg['from_id']
    role_id = users.get_role(user)
    globals()[command](msg=msg, chat=chat, role_id=role_id)
    return


def role(**kwargs):
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
            vk_api.send(kwargs['chat'], "No reply or forward")
            return

    if user_id < 0:
        vk_api.send(kwargs['chat'], "Only users can have roles")
        return

    kwargs['role_id'] = int(command[1])
    if kwargs['role_id'] < 0 or kwargs['role_id'] > 13:
        vk_api.send(kwargs['chat'], "Wrong role id")
        return
    else:
        users.set_role(user_id, kwargs['role_id'])
        vk_api.send(kwargs['chat'], "Role set!")
    return


def role_list(**kwargs):
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    r_list = users.get_roles()
    message = ''
    for i in r_list:
        message = message + i + '\n'
    vk_api.send(kwargs['msg']['from_id'], message)
    vk_api.send(kwargs['chat'], "List sent in your kwargs['chat'")
    return


def ping(**kwargs):
    roles = [0, 1, 4]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    vk_api.send(kwargs['chat'], "Still Alive")
    return


def test(**kwargs):
    vk_api.send(kwargs['chat'], kwargs['msg'])
    return


def kill(**kwargs):
    raise Exception


def kbda(**kwargs):
    # in multiThreading
    vk_api.send(kwargs['chat'], kwargs['msg'])
    return


def id(**kwargs):
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    if 'reply_message' in kwargs['msg'].keys():
        vk_api.send(kwargs['chat'], kwargs['msg']['reply_message']['from_id'])
        return kwargs['msg']['reply_message']['from_id']
    elif len(kwargs['msg']['fwd_messages']) == 1:
        vk_api.send(kwargs['chat'], kwargs['msg']['fwd_messages'][0]['from_id'])
        return
    else:
        vk_api.send(kwargs['chat'], kwargs['msg']['peer_id'])
        return


def kbd(**kwargs):
    vk_api.send(kwargs['chat'], "keyboard")
    return


def reg_squad(**kwargs):
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    cmd = kwargs['msg']['text'].split()

    if len(cmd) != 3:
        vk_api.send(kwargs['chat'], "Wrong arguments, squad and token needed")
        return

    if len(cmd[1]) > 2:
        vk_api.send(kwargs['chat'], "Use initials of squad (xx) for squad name")
        return
    cmd[1] = cmd[1].upper()

    if len(cmd[2]) != 128 or not hw_api.check(cmd[1], cmd[2]):
        vk_api.send(kwargs['chat'], "Wrong token")
        return
    else:
        squads.reg_squad(cmd[1], cmd[2])
        vk_api.send(kwargs['chat'], "Squad registered successfully")
    return


def target(**kwargs):
    roles = [0, 1, 3, 5, 7]
    # in multiThreading

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    cmd = kwargs['msg']['text'].split()

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        if len(cmd) == 3:

            cmd[1] = cmd[1].upper()
            if cmd[1] not in squads.get_squads():
                vk_api.send(kwargs['chat'], "Wrong source")
                return

            try:
                cmd[2] = int(cmd[2])
            except ValueError:
                vk_api.send(kwargs['chat'], "Wrong target, should be number")
                return

            if 0 <= cmd[2] <= 7:
                if cmd[2] == fraction:
                    vk_api.send(kwargs['chat'], 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(kwargs['chat'], 'Wrong target')
                return

            hw_api.set_target(cmd[1], cmd[2])
            return

        elif len(cmd) == 2:

            try:
                cmd[1] = int(cmd[1])
            except ValueError:
                vk_api.send(kwargs['chat'], "Wrong target, should be number")
                return

            if 0 <= cmd[1] <= 7:
                if cmd[1] == fraction:
                    vk_api.send(kwargs['chat'], 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(kwargs['chat'], 'Wrong target')
                return

            hw_api.set_target(str(fraction), cmd[1])
            vk_api.send(kwargs['chat'], "target sent!")
            return

        else:
            vk_api.send(kwargs['chat'], "Wrong arguments, (source and) target needed")
            return

    # Squad Leader
    else:
        if len(cmd) != 2:
            vk_api.send(kwargs['chat'], "Wrong arguments, target needed")
            return

        try:
            cmd[1] = int(cmd[1])
        except ValueError:
            vk_api.send(kwargs['chat'], "Wrong target, should be number")
            return

        if 0 <= cmd[1] <= 7:
            if cmd[1] == fraction:
                vk_api.send(kwargs['chat'], 'Attack on yourself')
                return
        else:
            # target = -1 or 9
            vk_api.send(kwargs['chat'], 'Wrong target')
            return

        source = users.get_squad(kwargs['msg']['from_id'])
        hw_api.set_target(source, cmd[1])
        vk_api.send(kwargs['chat'], "target sent!")
        return
