import vk_api
import hw_api
import settings

import db


def start(msg, command):
    chat = msg['peer_id']
    globals()[command](msg, chat)
    return


def test(msg, chat):
    vk_api.send(chat, msg)
    return


def kbda(msg, chat):
    # in multiThreading
    hw_api.remove_all()
    return


def id(msg, chat):
    if 'reply_message' in msg.keys():
        vk_api.send(chat, msg['reply_message']['from_id'])
        return msg['reply_message']['from_id']
    elif len(msg['fwd_messages']) == 1:
        vk_api.send(chat, msg['fwd_messages'][0]['from_id'])
        return msg['fwd_messages'][0]['from_id']
    else:
        vk_api.send(chat, msg['peer_id'])
        return msg['peer_id']


def kbd(msg, chat):
    return


def target(msg, chat):
    roles = [0, 1, 3, 5, 7]
    # in multiThreading

    user = msg['from_id']
    role_user = db.users.get_role(user)

    if role_user not in roles:
        vk_api.send(chat, "Access Denied")
        return

    cmd = msg['text'].split()

    # TeamLeader
    if role_user in roles[0:3]:
        if len(cmd) == 3:

            cmd[1] = cmd[1].upper()
            if cmd[1] not in db.squads.get_squads():
                vk_api.send(chat, "Wrong source")
                return

            try:
                cmd[2] = int(cmd[2])
            except ValueError:
                vk_api.send(chat, "Wrong target, should be number")
                return

            if 0 <= cmd[2] <= 7:
                if cmd[2] == settings.fraction:
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
                cmd[2] = int(cmd[2])
            except ValueError:
                vk_api.send(chat, "Wrong target, should be number")
                return

            if 0 <= cmd[2] <= 7:
                if cmd[2] == settings.fraction:
                    vk_api.send(chat, 'Attack on yourself')
                    return
            else:
                # target = -1 or 9
                vk_api.send(chat, 'Wrong target')
                return

            hw_api.set_target(settings.fraction, cmd[2])
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
            if cmd[1] == settings.fraction:
                vk_api.send(chat, 'Attack on yourself')
                return
        else:
            # target = -1 or 9
            vk_api.send(chat, 'Wrong target')
            return

        source = db.users.get_squad(user)
        hw_api.set_target(source, cmd[1])
        return
