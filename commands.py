import vk_api
import hw_api
import settings


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
    # in multiThreading

    user = msg['from_id']
    cmd = msg['text'].split()
    cmd[1] = cmd[1].upper()

    if settings.LO[user] == '3':
        # if not 3, like other LO
        if len(cmd) == 3:
            if cmd[1] in settings.squad_list.keys():
                if 0 <= cmd[2] <= 7:
                    if cmd[2] != 3:
                        hw_api.set_target(cmd[1], 0)
                    else:
                        # target = 3
                        vk_api.send(chat, 'Attack on yourself')
                        return
                else:
                    # target = -1 or 9
                    vk_api.send(chat, 'Wrong target')
                    return
            else:
                # target ?? 2
                vk_api.send(chat, 'Wrong source')
                return

    if len(cmd) == 2:
        if 0 <= cmd[1] <= 7:
            if cmd[1] != 3:
                hw_api.set_target(settings.LO[user], 0)
            else:
                # target = 3
                vk_api.send(chat, 'Attack on yourself')
                return
        else:
            # target = -1 or 9
            vk_api.send(chat, 'Wrong target')
            return
    else:
        # target what what WHAT
        vk_api.send(chat, 'Wrong params')
        return
