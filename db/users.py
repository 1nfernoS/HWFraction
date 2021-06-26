import datetime
from datetime import date as dt
import time

from db.db_sql import query
from db.squads import _validate_source
from settings import fraction


# TODO: valid_user/date/stats/etc(?)


def _validate_user(user_id):
    """
    Check that user_id is valid for vk
    :param user_id: int
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    """
    try:
        user_id = int(user_id)
    except ValueError:
        raise TypeError("user_id is not int")

    if user_id < 0 or user_id > 2000000000:
        # not bot and not chat
        raise ValueError("user_id below 0 or higher 2000000000")
    return


def update_msg(user_id, msg_time):
    """
    Write new time of last message into DB
    :param user_id: int, id vk [from_id]
    :param msg_time: int, unix time vk [date]
    :raise KeyError - user_id doesn't in DB
    :raise ValueError - wrong time value
    :raise TypeError - wrong time type (or can't be cast to type)
    """
    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] == 0:
        raise KeyError('user_id doesn\'t exists')

    try:
        msg_time = int(msg_time)
    except ValueError:
        raise TypeError("time should be int type")

    if msg_time < 0:
        raise ValueError("time can't be negative")

    if msg_time > time.time():
        raise ValueError("time can't be from future")

    query('UPDATE t_user SET c_last_message = %s WHERE c_id_user = %s', msg_time, user_id)

    return


# Overall user's handler
def reg_user(user_id):
    """
    Adds new user into DB
    :param user_id: id vk [from_id]
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    """
    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] != 0:
        raise KeyError('user_id already exists')

    values = (user_id, fraction, dt.min)
    query('INSERT INTO t_user VALUE (%s, 8, 0, 0, 0, "Аноним", 0, %s, 0, 0, 0, 0, %s, 0, 0, 0, 0);', values)
    return


def get_user(user_id):
    """
    Get user data from DB by vk_id [from_id]
    :param user_id: int, id from vk
    :return: dict, {user_id: int,
                    role_id: int,
                    subscribe: bool,
                    show_profile: bool,
                    show_report: bool,
                    nickname: str,
                    lvl: int,
                    squad: str,
                    practice: int,
                    theory: int,
                    guile: int,
                    wisdom: int,
                    date_report: datetime,
                    income: int,
                    pure_income: int,
                    target: int,
                    last_message: int}
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    :raise KeyError - user not in DB
    """
    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] == 0:
        raise KeyError('user_id doesn\'t exists')

    user_data = query('SELECT * FROM t_user WHERE c_id_user = %s', user_id)[0]
    user = {'user_id': int(user_data[0]),
            'role_id': int(user_data[1]),
            'subscribe': bool(user_data[2]),
            'show_profile': bool(user_data[3]),
            'show_report': bool(user_data[4]),
            'nickname': str(user_data[5]),
            'lvl': int(user_data[6]),
            'squad': str(user_data[7]),
            'practice': int(user_data[8]),
            'theory': int(user_data[9]),
            'guile': int(user_data[10]),
            'wisdom': int(user_data[11]),
            'date_report': user_data[12],
            'income': int(user_data[13]),
            'pure_income': int(user_data[14]),
            'target': int(user_data[15]),
            'last_message': int(user_data[16])}
    return user


def del_user(user_id):
    """
    Delete user from DB by id
    :param user_id: int, id vk [from_id]
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    """
    _validate_user(user_id)

    query('DELETE FROM t_user WHERE c_id_user = %s;', user_id)
    return


# User's profile handler
def set_profile(user_id, nick, lvl, squad, prac, teo, hit, mud):
    """
    Updates user's profile data in DB by id
    :param user_id: int, id vk [from_id]
    :param nick: str
    :param lvl: int
    :param squad: str(2)
    :param prac: int
    :param teo: int
    :param hit: int
    :param mud: int
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    :raise KeyError - user or squad not in DB
    """
    def _validate_stats(stat):
        """
        Check stats before input
        :param stat: int, stat param to check
        :return: int, stat parameter
        :raise TypeErrorwrong type (or can't be cast to type)
        :raise ValueError - wrong value
        """
        try:
            stat = int(stat)
        except ValueError:
            raise TypeError("Some stt is not int type")
        if stat < 0:
            raise ValueError("Stat can't be negative")
        return stat

    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] == 0:
        raise KeyError('user_id doesn\'t exists')

    # nick and squad can't raise ValueError, so just str them
    nick = str(nick)
    if len(nick) < 3 or len(nick) > 25:
        raise ValueError('nickname should be in length 3-25')

    _validate_stats(lvl)

    _validate_source(squad)

    prac, teo, hit, mud = _validate_stats(prac), _validate_stats(teo), _validate_stats(hit), _validate_stats(mud)

    args = (nick, lvl, squad, prac, teo, hit, mud, user_id)
    query('UPDATE t_user '
          'SET c_nickname = %s, c_level = %s, c_squad = %s, c_practice = %s, c_theory = %s, c_guile = %s, c_wisdom = %s'
          ' WHERE c_id_user = %s;', args)

    return


def set_report(user_id, dat, inc, pure, target):
    """
    Updates Battle report of user in DB
    :param user_id: inv, id vk [from_id]
    :param dat: date
    :param inc: int, income from battle
    :param pure: int, pure income
    :param target: int, fraction (0-7)
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    :raise KeyError - user_id not in DB
    """
    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] == 0:
        raise KeyError('user_id doesn\'t exists')

    if type(dat) != dt:
        try:
            dat = dat.date()
        except AttributeError:
            raise TypeError("date is not datetime.date")
    now = datetime.datetime.utcnow()
    yest = dt.today() - datetime.timedelta(days=1)
    battle = datetime.time(15)
    if dat > now.date():
        raise ValueError("date can't be from future")
    if now.time() < battle:
        if dat < yest:
            raise ValueError("date is too old")
    else:
        if dat < now.date():
            raise ValueError("date is too old")

    try:
        inc = int(inc)
    except ValueError:
        raise TypeError("income is not int")

    try:
        pure = int(pure)
    except ValueError:
        raise TypeError("pure income is not int")

    if inc > 0:
        if pure > inc:
            raise ValueError("pure income can\'t be greater than overall income")
    else:
        if pure != 0:
            raise ValueError("pure income can\'t be non-zero if overall income negative")

    try:
        target = int(target)
    except ValueError:
        raise TypeError("target is not int")
    if target < 0 or target > 7:
        raise ValueError("target must be in range 0-7")
    if target == fraction:
        raise ValueError("target can\'t be own fraction")

    # insert data
    args = (dat, inc, pure, target, user_id)
    query('UPDATE t_user '
          'SET c_date_report = %s, c_income = %s, c_pure_income = %s, c_target = %s '
          'WHERE c_id_user = %s', args)
    return


def change_preference(user_id, key):
    """
    Toggles preference in DB by id and key
    :param user_id: int, id vk [from_id]
    :param key: str, ['subscribe', 'profile', 'report']
    :raise ValueError - wrong value
    :raise TypeError - wrong type (or can't be cast to type)
    :raise KeyError - user_id or preference not in DB
    """
    _validate_user(user_id)

    if query('SELECT COUNT(*) FROM t_user WHERE c_id_user = %s', user_id)[0][0] == 0:
        raise KeyError('user_id doesn\'t exists')

    key = str(key)
    keys = {'subscribe': 'c_is_subscribed', 'profile': 'c_show_profile', 'report': 'c_show_report'}
    if key not in keys.keys():
        raise KeyError("There is no preference %s" % key)

    state = query("SELECT " + keys[key] + " FROM t_user WHERE c_id_user = %s", user_id)[0][0]
    query("UPDATE t_user SET " + keys[key] + " = %s WHERE c_id_user = %s", not bool(state), user_id)
    return
