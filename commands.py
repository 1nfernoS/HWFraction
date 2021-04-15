import vk_api
import hw_api
from settings import fraction

import db.users as users
import db.squads as squads


def start(msg, command):
    chat = msg['peer_id']
    globals()[command](msg, chat)
    return


def role(msg, chat):
    roles = [0]

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    command = msg['text'].split()
    if len(command) != 2:
        vk_api.send(chat, "Wrong arguments, role id needed")
        return
    if 'reply_message' in msg.keys():
        user_id = msg['reply_message']['from_id']
    else:
        if len(msg['fwd_messages']) == 1:
            user_id = msg['fwd_messages'][0]['from_id']
        else:
            vk_api.send(chat, "No reply or forward")
            return

    if user_id < 0:
        vk_api.send(chat, "Only users can have roles")
        return

    role_id = int(command[1])
    if role_id < 0 or role_id > 13:
        vk_api.send(chat, "Wrong role id")
        return
    else:
        users.set_role(user_id, role_id)
        vk_api.send(chat, "Role set!")
    return


def role_list(msg, chat):
    roles = [0]

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    r_list = users.get_roles()
    msg = ''
    for i in r_list:
        msg = msg + i + '\n'
    vk_api.send(user, msg)
    vk_api.send(chat, "List sent in your chat")
    return


def ping(msg, chat):
    roles = [0, 1, 4]

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    vk_api.send(chat, "Still Alive")
    return


def test(msg, chat):
    vk_api.send(chat, msg)
    return


def kill(msg, chat):
    raise Exception


def kbda(msg, chat):
    # in multiThreading
    vk_api.send(chat, msg)
    return


def id(msg, chat):
    roles = [0]

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    if 'reply_message' in msg.keys():
        vk_api.send(chat, msg['reply_message']['from_id'])
        return msg['reply_message']['from_id']
    elif len(msg['fwd_messages']) == 1:
        vk_api.send(chat, msg['fwd_messages'][0]['from_id'])
        return
    else:
        vk_api.send(chat, msg['peer_id'])
        return


def kbd(msg, chat):
    vk_api.send(chat, msg)
    return


def reg_squad(msg, chat):
    # TeamLeaders only
    roles = [0, 1, 3]

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    cmd = msg['text'].split()

    if len(cmd) != 3:
        vk_api.send(chat, "Wrong arguments, squad and token needed")
        return

    if len(cmd[1]) > 2:
        vk_api.send(chat, "Use initials of squad (xx) for squad name")
        return
    cmd[1] = cmd[1].upper()

    if len(cmd[2]) != 128 or not hw_api.check(cmd[1], cmd[2]):
        vk_api.send(chat, "Wrong token")
        return
    else:
        squads.reg_squad(cmd[1], cmd[2])
        vk_api.send(chat, "Squad registered successfully")
    return


def target(msg, chat):
    roles = [0, 1, 3, 5, 7]
    # in multiThreading

    user = msg['from_id']
    role_user = users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    cmd = msg['text'].split()

    # TeamLeader
    if role_user in roles[0:3]:
        if len(cmd) == 3:

            cmd[1] = cmd[1].upper()
            if cmd[1] not in squads.get_squads():
                vk_api.send(chat, "Wrong source")
                return

            try:
                cmd[2] = int(cmd[2])
            except ValueError:
                vk_api.send(chat, "Wrong target, should be number")
                return

            if 0 <= cmd[2] <= 7:
                if cmd[2] == fraction:
                    vk_api.send(chat, 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(chat, 'Wrong target')
                return

            hw_api.set_target(cmd[1], cmd[2])
            return

        elif len(cmd) == 2:

            try:
                cmd[1] = int(cmd[1])
            except ValueError:
                vk_api.send(chat, "Wrong target, should be number")
                return

            if 0 <= cmd[1] <= 7:
                if cmd[1] == fraction:
                    vk_api.send(chat, 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(chat, 'Wrong target')
                return

            hw_api.set_target(str(fraction), cmd[1])
            vk_api.send(chat, "target sent!")
            return

        else:
            vk_api.send(chat, "Wrong arguments, (source and) target needed")
            return

    # Squad Leader
    else:
        if len(cmd) != 2:
            vk_api.send(chat, "Wrong arguments, target needed")
            return

        try:
            cmd[1] = int(cmd[1])
        except ValueError:
            vk_api.send(chat, "Wrong target, should be number")
            return

        if 0 <= cmd[1] <= 7:
            if cmd[1] == fraction:
                vk_api.send(chat, 'Attack on yourself')
                return
        else:
            # target = -1 or 9
            vk_api.send(chat, 'Wrong target')
            return

        source = users.get_squad(user)
        hw_api.set_target(source, cmd[1])
        vk_api.send(chat, "target sent!")
        return
