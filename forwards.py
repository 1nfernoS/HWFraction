"""
This module handles forwards in messages. If no case to process forwards, it will do nothing
Now there is not much info, so later I will expand it
def parse is entry point of module, other def-s are calls from it.
(c) Misden a.k.a. 1nfernos, 2021
"""
import re
import datetime
from settings import hw_id, errors_chat, fractions, fraction

import db.users as users
import vk_api
from hw_api import distribute


def parse(msg, fwd):
    roles = [0]
    user_id = msg['from_id']
    role_id = users.get_role(user_id)
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
                battle(user_id, txt, role_id)
            elif inventory_flag:
                return
            elif profile_flag:
                profile(user_id, txt, role_id)
            elif share_flag:
                share(user_id, txt, role_id)
            else:
                if role_id in roles:
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


def share(user_id, text, role_id):

    user_info = users.get_user(user_id)
    shar = text.split(sep='\n\n')

    tl_flag = False
    sl_flag = False

    nick_pattern = r"\b\w\w\w+\s"
    squad_pattern = r"\b\w\w\b"
    emoji_pattern = r"&#\d+;"
    stat_pattern = r"\s\d+"

    """
        Parse block
    """

    row = shar[0].split(sep='\n')[0]

    nick = re.search(nick_pattern, row)[0].strip()

    sl = '&#9643;'
    tl = '&#128312;'
    if sl in row:
        sl_flag = True
    elif tl in row:
        tl_flag = True
    else:
        pass

    f = fractions[re.findall(emoji_pattern, row)[-1]]

    if re.search(squad_pattern, row):
        squad = re.search(squad_pattern, row)[0]
    else:
        squad = f

    # TODO: Do smth with fraction

    prc_val = int(re.findall(stat_pattern, shar[1])[0])
    teo_val = int(re.findall(stat_pattern, shar[1])[1])
    hit_val = int(re.findall(stat_pattern, shar[1])[2])
    mud_val = int(re.findall(stat_pattern, shar[1])[3])

    # Check share with profile

    if nick != user_info['nickname']:
        vk_api.send(user_id, "Wrong Nickname, re-send profile to confirm")
        return

    if squad != user_info['squad']:
        vk_api.send(user_id, "Re-send profile to confirm squad")
        return

    if f != fraction:
        vk_api.send(user_id, "Send profile to confirm fraction")
        return

    message = str()
    message = message + nick + '\n'
    if tl_flag:
        message = message + "TL" + '\n'
    elif sl_flag:
        message = message + "SL" + '\n'
    else:
        message = message + "No Status" + '\n'
    message = message + str(f) + '\n'
    message = message + str(squad) + '\n'
    message = message + str(prc_val) + ', ' + str(teo_val) + '\n'
    message = message + str(hit_val) + ', ' + str(mud_val) + '\n'

    # If all ok, write new data in db

    users.set_profile(user_id, nick, squad, prc_val, teo_val, hit_val, mud_val)
    vk_api.send(user_id, "Share accepted!\n" + message)

    return


def profile(user_id, text, role_id):

    prof = text.split(sep='\n\n')[-3:-1]

    tl_flag = False
    sl_flag = False
    squad_flag = False

    nick_pattern = r"\b\w\w\w+\s"
    squad_pattern = r"\b\w\w\b"
    emoji_pattern = r"&#\d+;"
    full_pattern = r"\(\d+\)"
    short_pattern = r"\s\d+"

    """
        Parse block
    """

    row = prof[0].split(sep='\n')[0]

    nick = re.search(nick_pattern, row)[0].strip()

    sl = '&#9643;'
    tl = '&#128312;'
    if sl in row:
        sl_flag = True
    elif tl in row:
        tl_flag = True
    else:
        pass

    f = fractions[re.findall(emoji_pattern, row)[-1]]

    if re.search(squad_pattern, row):
        squad = re.search(squad_pattern, row)[0]
        squad_flag = True
    else:
        squad = f

    if len(re.findall(full_pattern, prof[1])) == 0:
        prc_val = int(re.findall(short_pattern, prof[1])[0])
        teo_val = int(re.findall(short_pattern, prof[1])[1])
        hit_val = int(re.findall(short_pattern, prof[1])[2])
        mud_val = int(re.findall(short_pattern, prof[1])[3])
    else:
        prc_val = int(re.findall(full_pattern, prof[1])[0][1:-1])
        teo_val = int(re.findall(full_pattern, prof[1])[1][1:-1])
        hit_val = int(re.findall(full_pattern, prof[1])[2][1:-1])
        mud_val = int(re.findall(full_pattern, prof[1])[3][1:-1])

    message = str()
    message = message + nick + '\n'
    if tl_flag:
        message = message + "TL" + '\n'
    elif sl_flag:
        message = message + "SL" + '\n'
    else:
        message = message + "No Status" + '\n'
    message = message + str(f) + '\n'
    message = message + str(squad) + '\n'
    message = message + str(prc_val) + ', ' + str(teo_val) + '\n'
    message = message + str(hit_val) + ', ' + str(mud_val) + '\n'

    # If all ok, write new data in db
    users.set_profile(user_id, nick, squad, prc_val, teo_val, hit_val, mud_val)

    roles = [0, 3, 4, 7, 8]  # Creator and associate leaders (no signs in profile for him)
    if tl_flag:
        if f == fraction:
            role = 1
        else:
            role = 2
    elif sl_flag:
        if f == fraction:
            role = 5
        else:
            role = 6
    elif squad_flag:
        role = 9
    elif f == fraction:
        role = 11
    else:
        role = 12
    if role_id != role and role_id not in roles:
        users.set_role(user_id, role)

    vk_api.send(user_id, "Profile accepted!\n" + message)

    return


def battle(user_id, text, role_id):
    roles = [0, 1, 3, 5, 7, 9, 11]

    if role_id not in roles:
        return

    date_row = text.split(sep='\n\n')[0]
    date_pattern = r"\d{2}.\d{2}.\d{4}"
    date = re.search(date_pattern, date_row)[0]
    date = datetime.datetime.strptime(date, '%d.%m.%Y').date()  # DD.MM.YYYY format

    tomorrow = datetime.date.today().replace(day=datetime.date.today().day+1)
    if date > tomorrow:
        vk_api.send(user_id, "Future reports are not allowed")
        return

    # TODO: Add check for date limit (for every squad or 3 days)

    last_report = users.get_report(user_id)['date']
    last_report = datetime.datetime.strptime(last_report, '%Y-%m-%d').date()
    if date < last_report:
        vk_api.send(user_id, "This is old report, send more actual")
        return

    money = r"\d+"
    emoji_pattern = r"&#\d+;"

    msg = text.split(sep='\n\n')[1:-1]
    income = 0
    pure = 0
    target = 0
    result = str()
    for block in range(len(msg)):
        res = msg[block].split(sep='\n')
        if len(res) == 1:
            target = 0
            result = result + 'AFK' + '\n'
        elif len(res) == 2:
            tran = int(re.search(money, res[1])[0])
            result = result + "Transaction:" + str(tran) + '\n'
            income += tran
            pure += tran
        elif len(res) == 3:
            loss = int(re.search(money, res[2])[0])
            result = result + "Lost from def:" + str(loss) + '\n'
            pure -= loss
        elif len(res) == 4:
            if re.search(emoji_pattern, res[0]):
                target = fractions[re.search(emoji_pattern, res[0])[0]]
            else:
                target = 7
            main = int(re.search(money, res[2])[0])
            result = result + "Failed attack: " + str(main) + '\n'
            pure -= main
        elif len(res) == 5:
            if re.search(emoji_pattern, res[0]):
                target = fractions[re.search(emoji_pattern, res[0])[0]]
            else:
                target = 7
            main = int(re.search(money, res[2])[0])
            result = result + "Attack: " + str(main) + '\n'
            pure += main
            income += main
    result = result + "Income:" + str(income) + '\nPure:' + str(pure) + '\nTarget:' + str(target)

    vk_api.send(user_id, result)

    users.set_report(user_id, date, income, pure, target)
    vk_api.send(user_id, "Battle result successfully written")
    return
