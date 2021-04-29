"""
This module handles forwards in messages. If no case to process forwards, it will do nothing
Now there is not much info, so later I will expand it
def parse is entry point of module, other def-s are calls from it.
(c) Misden a.k.a. 1nfernos, 2021
"""
from settings import hw_id, errors_chat, fractions

from db.users import get_role
import vk_api
from hw_api import distribute


def parse(msg, fwd):
    roles = [0]
    user_id = msg['from_id']
    role_id = get_role(user_id)
    chat_id = msg['peer_id']

    if len(fwd) == 1:
        # check some things
        if fwd[0]['from_id'] == hw_id:
            txt = str(fwd[0]['text']).encode('cp1251', 'xmlcharrefreplace').decode('cp1251')
            battle_flag = 'Результаты битвы за' in txt
            profile_flag = '&#128716;' in txt  # bed emoji
            share_flag = '&#128187;' in txt  # lvl emoji / notebook emoji
            inventory_flag = '&#127890;' in txt  # backpack emoji
            if battle_flag:
                print("forward with battle")
            elif inventory_flag:
                return
            elif profile_flag:
                profile(user_id, txt)
            elif share_flag:
                share(user_id, txt)
            elif role_id in roles:
                get_time(fwd, chat_id, role_id)
            return
        else:
            get_time(fwd, chat_id, role_id)
            return
    elif len(fwd) == 7:
        if chat_id < 2000000000:
            distribution(fwd, chat_id, role_id, user_id)
            return
        else:
            return
    # Exists:
    # +  return time in 1-3 forwards depth
    # +  start distribute res of battle if len==7 and all from bot
    #   return object if text = '/test' (ignore)
    # Needed to:
    #   parse profile, share
    #   react to battle stats
    return


def get_time(fwd, chat_id, role_id):
    roles = [0]  # maybe add testers
    if role_id not in roles:
        return
    if 'fwd_messages' in fwd[0].keys():
        if 'fwd_messages' in fwd[0]['fwd_messages'][0].keys():
            res = fwd[0]['fwd_messages'][0]['date']
        else:
            res = fwd[0]['date']
    else:
        res = fwd[0]['date']
    vk_api.send(chat_id, str(res))
    return


def distribution(fwd, chat_id, role_id, user_id):
    roles = [role_id]  # maybe here will be role limit
    if role_id not in roles:
        return
    message = str()
    for i in range(7):
        if fwd[i]['from_id'] == hw_id:
            message += str(fwd[i]['text']).replace('\n\n', '\n') + '\n\n'
        else:
            vk_api.send(errors_chat, "@id" + str(user_id) + " tried to distribute and have error\nMessage is:\n" + message)
            return
    distribute(message)
    vk_api.send(chat_id, "Request to distribute sent!")
    return


def share(user_id, text):

    # TODO: check share with profile
    shar = text.split(sep='\n\n')

    tl_flag = False
    sl_flag = False
    squad_flag = False

    # TODO: find a way to correct parse
    string = shar[0][:shar[0].find('\n')]
    if string.find(';')+1 > string.find(' ('):
        start = 0
    else:
        start = string.find(';')+1
    end = string.find(' (')
    nick = string[start:end]
    string = string[string.find('(')+1:string.find(')')]
    sl = '&#9643;'
    tl = '&#128312;'
    if sl in string:
        sl_flag = True
        string = string.replace(sl, '')
    elif tl in string:
        tl_flag = True
        string = string.replace(tl, '')
    else:
        pass

    if string.find('|') != -1:
        squad = string[:2]
        squad_flag = True
        string = string[5:]

    # TODO: Do smth with fraction
    frac = string[:string.find(';')+1]
    fraction = fractions[frac]

    string = shar[1]
    stats = string.split(sep='\n')
    prac_val = int(stats[0].split(sep='; ')[0][stats[0].split(sep='; ')[0].find(':')+2:])
    teo_val = int(stats[0].split(sep='; ')[1][stats[0].split(sep='; ')[0].find(':')+2:])
    hit_val = int(stats[1].split(sep='; ')[0][stats[0].split(sep='; ')[0].find(':')+2:])
    mud_val = int(stats[1].split(sep='; ')[1][stats[0].split(sep='; ')[0].find(':')+2:])

    message = str()
    message = message + nick + '\n'
    if tl_flag:
        message = message + "TL" + '\n'
    elif sl_flag:
        message = message + "SL" + '\n'
    else:
        message = message + "No Status" + '\n'
    message = message + str(fraction) + '\n'
    if squad_flag:
        message = message + str(squad) + '\n'
    else:
        message = message + str(fraction) + '\n'
    message = message + str(prac_val) + ', ' + str(teo_val) + '\n'
    message = message + str(hit_val) + ', ' + str(mud_val) + '\n'

    vk_api.send(user_id, message)

    # TODO: If all ok, write new data in db
    return


def profile(user_id, text):

    prof = text.split(sep='\n\n')[-3:-1]

    tl_flag = False
    sl_flag = False
    squad_flag = False

    # TODO: find a way to correct parse
    string = prof[0][:prof[0].find('\n')]
    if string.find(';')+1 > string.find(' ('):
        start = 0
    else:
        start = string.find(';')+1
    end = string.find(' (')
    nick = string[start:end]
    string = string[string.find('(')+1:string.find(')')]
    sl = '&#9643;'
    tl = '&#128312;'
    if sl in string:
        sl_flag = True
        string = string.replace(sl, '')
    elif tl in string:
        tl_flag = True
        string = string.replace(tl, '')
    else:
        pass

    if string.find('|') != -1:
        squad = string[:2]
        squad_flag = True
        string = string[5:]

    # TODO: Do smth with fraction
    frac = string[:string.find(';')+1]
    fraction = fractions[frac]

    string = prof[1]
    stats = string.split(sep='\n')
    if len(stats) == 2:
        prac_val = int(stats[0].split(sep='; ')[0][stats[0].split(sep='; ')[0].find(':')+2:])
        teo_val = int(stats[0].split(sep='; ')[1][stats[0].split(sep='; ')[0].find(':')+2:])
        hit_val = int(stats[1].split(sep='; ')[0][stats[0].split(sep='; ')[0].find(':')+2:])
        mud_val = int(stats[1].split(sep='; ')[1][stats[0].split(sep='; ')[0].find(':')+2:])
    else:
        prac_val = int(stats[1][stats[1].find('(')+1:stats[1].find(')')])
        teo_val = int(stats[2][stats[2].find('(')+1:stats[2].find(')')])
        hit_val = int(stats[3][stats[3].find('(')+1:stats[3].find(')')])
        mud_val = int(stats[4][stats[4].find('(')+1:stats[4].find(')')])

    message = str()
    message = message + nick + '\n'
    if tl_flag:
        message = message + "TL" + '\n'
    elif sl_flag:
        message = message + "SL" + '\n'
    else:
        message = message + "No Status" + '\n'
    message = message + str(fraction) + '\n'
    if squad_flag:
        message = message + str(squad) + '\n'
    else:
        message = message + str(fraction) + '\n'
    message = message + str(prac_val) + ', ' + str(teo_val) + '\n'
    message = message + str(hit_val) + ', ' + str(mud_val) + '\n'

    vk_api.send(user_id, message)

    # TODO: If all ok, write new data in db
    return


def battle():
    return
