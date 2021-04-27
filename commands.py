from threading import Thread

import vk_api
import hw_api
from settings import fraction, start_time

import db.users as users
import db.squads as squads


def start(msg, command):
    chat = msg['peer_id']
    user_id = msg['from_id']
    role_id = users.get_role(user_id)
    globals()[command](msg=msg, chat=chat, role_id=role_id)
    return


def cmd_list(**kwargs):
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    cmd = list(globals())[15:-1]
    msg = 'There are ' + str(len(cmd)) + ' commands:\n'
    for i in cmd:
        msg = msg + i + '\n'
    vk_api.send(kwargs['chat'], msg)

    return


def user(**kwargs):
    roles = [0, 1, 3, 5, 7]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    # TeamLeader
    if kwargs['role_id'] in roles[0:3]:
        cmd = kwargs['msg']['text'].split()
        if len(cmd) == 2:
            cmd[1] = cmd[1].upper()
            if cmd[1] not in squads.get_squads():
                vk_api.send(kwargs['chat'], "Wrong squad")
                return
            squad_users = squads.squad_users(cmd[1])
            msg = ''
            for i in squad_users:
                msg = msg + '[id' + str(i) + '|' + str(squad_users[i]) + ']\n'
            if msg == '':
                vk_api.send(kwargs['chat'], "Empty...")
            else:
                vk_api.send(kwargs['chat'], msg)
            return
        elif len(cmd) == 1:
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
    if users.count_role(role_id) < role_limit[role_id]:
        users.set_role(user_id, role_id)
        vk_api.send(kwargs['chat'], "Role set!")
    else:
        vk_api.send(kwargs['chat'], "Limit of Role!")
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
    vk_api.send(kwargs['chat'], "List sent in your chat")
    return


def ping(**kwargs):
    roles = [0, 1, 4]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    vk_api.send(kwargs['chat'], "Still Alive from " + str(int(start_time)))
    return


def test(**kwargs):
    vk_api.send(kwargs['chat'], kwargs['msg'])
    return


def delete(**kwargs):
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
    roles = [0]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    raise Exception


def kbda(**kwargs):
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return
    Thread(target=hw_api.remove_all).run()
    vk_api.send(kwargs['chat'], "Keyboards are removed")
    return


def id(**kwargs):
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
    # TeamLeaders only
    roles = [0, 1, 3]

    if kwargs['role_id'] not in roles:
        vk_api.send(kwargs['chat'], "Access Denied")
        return

    keyboard = {'one_time': False, 'buttons': [
        [
            {'action': {'type': 'text', 'label': '&#128160; Aegis', 'payload': '{"target": 1}'},
             'color': 'primary'},
            {'action': {'type': 'text', 'label': '&#128679; V-Hack', 'payload': '{"target": 2}'},
             'color': 'primary'},
            {'action': {'type': 'text', 'label': '&#127541; Hu&#466;qi&#225;ng', 'payload': '{"target": 4}'},
             'color': 'primary'}
        ],
        [
            {'action': {'type': 'text', 'label': '&#128305; NetKings', 'payload': '{"target": 5}'},
             'color': 'primary'},
            {'action': {'type': 'text', 'label': '&#127482;&#127480; NHS', 'payload': '{"target": 6}'},
             'color': 'primary'},
            {'action': {'type': 'text', 'label': '&#128272; Защита', 'payload': '{"target": 7}'},
             'color': 'secondary'}
        ],
        [
            {'action': {'type': 'text', 'label': '&#10060; Удалить клавиатуру', 'payload': '{"target": 0}'},
             'color': 'negative'}
        ]]}
    vk_api.send(kwargs['chat'], "Your keyboard!", keyboard)
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
        vk_api.send(kwargs['chat'], "Wrong token or squad")
        return
    else:
        squads.reg_squad(cmd[1], cmd[2])
        vk_api.send(kwargs['chat'], "Squad registered successfully")
    return


def target(**kwargs):
    roles = [0, 1, 3, 5, 7]

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

            Thread(target=hw_api.set_target, args=(cmd[1], cmd[2])).run()
            vk_api.send(kwargs['chat'], "Target sent!")
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

            Thread(target=hw_api.set_target, args=(str(fraction), cmd[1])).run()
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
        Thread(target=hw_api.set_target(), args=(source, cmd[1])).run()
        vk_api.send(kwargs['chat'], "target sent!")
        return


def dist(msg):
    Thread(target=hw_api.distribute, args=(msg,)).run()
    return
