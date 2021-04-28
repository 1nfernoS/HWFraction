"""
This module handles forwards in messages. If no case to process forwards, it will do nothing
Now there is not much info, so later I will expand it
def parse is entry point of module, other def-s are calls from it.
(c) Misden a.k.a. 1nfernos, 2021
"""
import threading

from settings import hw_id, errors_chat, fractions

from db.users import get_role
import vk_api
from hw_api import distribute


def parse(msg, fwd):
    user_id = msg['from_id']
    role_id = get_role(user_id)
    chat_id = msg['peer_id']

    if len(fwd) == 1:
        # check some things
        if fwd[0]['from_id'] == hw_id:
            txt = str(fwd[0]['text'])
            battle_flag = 'Результаты битвы за' in txt
            profile_flag = '&#128181;' in txt or '💵' in txt  # money emoji
            share_flag = '&#128187;' in txt or '💻' in txt  # lvl emoji / notebook emoji
            inventory_flag = '&#127890;' in txt or '🎒' in txt  # backpack emoji
            vk_api.send(errors_chat, "@id" + str(user_id) + " sent forward from hw, battle: " + str(battle_flag) +
                        ", profile: " + str(profile_flag) + ", share: " + str(share_flag) + ", inventory: " +
                        str(inventory_flag))
            if battle_flag:
                print("forward with battle")
            elif inventory_flag:
                return
            elif profile_flag:
                profile(user_id, fwd[0]['text'])
            elif share_flag:
                share(user_id, fwd[0]['text'])
            else:
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
    threading.Thread(target=distribute, args=(message,)).start()
    vk_api.send(chat_id, "Request to distribute sent!")
    return


def share(user_id, text):

    # TODO: check share with profile
    tl_flag = False
    sl_flag = False
    squad_flag = False

    if text.find(';')+1 > text.find(' ('):
        start = 0
    else:
        start = text.find(';')+1
    end = text.find(' (')
    nick = text[start:end]

    sl = '&#9643;'
    tl = '&#128312;'
    if sl in text:
        sl_flag = True
    elif tl in text:
        tl_flag = True
    else:
        pass

    if text.find('|') != -1:
        if tl_flag:
            squad = text[text.find(tl) + 9:text.find('|')]
        elif sl_flag:
            squad = text[text.find(sl) + 7:text.find('|')]
        else:
            squad = text[text.find('(')+1:text.find('|')]
        squad_flag = True

        start = text.find('|') + 2
        end = start + text[start:].find(';')
    else:
        if tl_flag:
            start = text.find(tl) + 9
        else:
            start = text.find('(') + 1

        end = start + text[start:].find(';')

    # TODO: Do smth with fraction
    fraction = fractions[text[start:end+1].strip()]

    prac = '&#128225;'
    start = text.find(prac)+11
    end = start + text[start:].find(';')
    prac_val = int(text[start:end])

    teo = '&#128190;'
    start = text.find(teo) + 11
    end = start + text[start:].find('\n')
    teo_val = int(text[start:end])

    hit = '&#128241;'
    start = text.find(hit) + 11
    end = start + text[start:].find(';')
    hit_val = int(text[start:end])

    mud = '&#128270;'
    start = text.find(mud) + 11
    mud_val = int(text[start:])

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

    if '&#128181;Деньги:' in text:
        short = False
    else:
        short = True

    if short:
        min_start = text[:-150].rfind('\n\n') + 2
    else:
        min_start = text[:-250].rfind('\n\n') + 2
    text = text[min_start:]

    tl_flag = False
    sl_flag = False
    squad_flag = False

    # TODO: find a way to correct parse
    if text.find(';')+1 > text.find(' ('):
        min_start = 0
    else:
        min_start = text.find(';')+1
    end = text.find(' (')
    nick = text[min_start:end]

    sl = '&#9643;'
    tl = '&#128312;'
    if sl in text:
        sl_flag = True
    elif tl in text:
        tl_flag = True
    else:
        pass

    if text.find('|') != -1:
        if tl_flag:
            squad = text[text.find(tl) + 9:text.find('|')]
        elif sl_flag:
            squad = text[text.find(sl) + 7:text.find('|')]
        else:
            squad = text[text.find('(')+1:text.find('|')]
        squad_flag = True

        start = text.find('|') + 2
        end = start + text[start:].find(';')
    else:
        if tl_flag:
            start = text.find(tl) + 9
        else:
            start = text.find('(') + 1

        end = start + text[start:].find(';')

    # TODO: Do smth with fraction
    fraction = fractions[text[start:end+1].strip()]

    if short:
        prac = '&#128225;: '
        start = text.find(prac)+11
        end = start + text[start:].find(';')
    else:
        prac = '&#128225;Практика: '
        start = text.find(prac) + 11
        start = start + text[start:].find('(') + 1
        end = start + text[start:].find(')')
    prac_val = int(text[start:end])

    if short:
        teo = '&#128190;: '
        start = text.find(teo) + 11
        end = start + text[start:].find('\n')
    else:
        teo = '&#128190;Теория: '
        start = text.find(teo) + 11
        start = start + text[start:].find('(') + 1
        end = start + text[start:].find(')')
    teo_val = int(text[start:end])

    if short:
        hit = '&#128241;: '
        start = text.find(hit) + 11
        end = start + text[start:].find(';')
    else:
        hit = '&#128241;Хитрость: '
        start = text.find(hit)
        start = start + text[start:].find('(') + 1
        end = start + text[start:].find(')')
    hit_val = int(text[start:end])

    if short:
        mud = '&#128270;: '
        start = text.find(mud) + 11
        end = start + text[start:].find('\n')
    else:
        mud = '&#128270;Мудрость: '
        start = text.find(mud) + 11
        start = start + text[start:].find('(') + 1
        end = start + text[start:].find(')')
    mud_val = int(text[start:end])

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
