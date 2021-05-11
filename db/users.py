"""
This module works with player's entity in database - mainly in 3 tables, which contains main info
If you want to work with all entity - use vUser view. Remember, this will work with SELECT statements only.
Make different def-s to INSERT, DELETE and SELECT, and don't forget to have all 3 def-s (if it needed)
Don't forget to try convert data type (for simplify errors)
    and check data type for excepting MySQL Errors (Trust me, you don't want to drop database)
(c) Misden a.k.a. 1nfernos, 2021
"""
from mysql.connector.errors import IntegrityError
import datetime
import time

from settings import fraction
from db.db_sql import db_open, db_close, get_columns
from db.squads import get_squads


def reg_user(user_id, last_msg_time):
    """
    Add new user into DB
    :param user_id: int, id from vk [from_id]
    :param last_msg_time: int, unix time [date]
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(last_msg_time) != int:
        try:
            last_msg_time = int(last_msg_time)
        except ValueError:
            raise TypeError("Time should be int type")
    elif last_msg_time > int(time.time()):
        raise ValueError("Time should have lesser value than now (unix)")

    data = (user_id, last_msg_time)
    query = 'INSERT INTO tPreferences (cIdUser, cIsSubscribed, cIsReported, cShowProfile, cShowReport, cLastMsg) ' \
            'VALUE (%s, FALSE, FALSE, FALSE, FALSE, %s);'

    db, cursor = db_open()

    try:
        cursor.execute(query, data)
        db.commit()

        set_profile(user_id, 'Аноним', None, 0, 0, 0, 0)
        set_report(user_id, datetime.date.min, 0, 0, 0)

        db_close(db, cursor)

    except IntegrityError:
        # This can occur if not all 3 tables from vUser have row, so it will re-register him

        db_close(db, cursor)

        del_user(user_id)
        reg_user(user_id, last_msg_time)

    change_preference(user_id, 'cIsReported')

    return


def user_list():
    """
    Get user_id and role_id from DB
    [WARNING] Deprecated due to big quantity of data
    :return: dict {user: role}
    """
    query = 'SELECT cIdUser, cIdRole FROM vUser;'

    db, cursor = db_open()

    cursor.execute(query)
    res = cursor.fetchall()

    db_close(db, cursor)

    employee = dict()

    for r in res:
        employee[r[0]] = r[1]

    return employee


def get_user(user_id):
    """
    Get all info about user from DB
    :param user_id: int, user id from vk [from_id]
    :return: dict {user_id: int, role: int,
    subscribe: bool, report: bool, show_profile: bool, show_report: bool,
    nickname: str, squad: str, practice: int, theory: int, guile: int, wisdom: int;
    if report True: date_report: str, income: int, pure_income: int, target: int}
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM vUser WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        raise ValueError("User doesn't exist, try to reg him first")
    res = res[0]

    user = dict()
    user['user_id'] = res[0]
    user['role'] = res[1] if res[1] is not None else 12
    user['subscribe'] = bool(res[2])
    user['report'] = bool(res[3])
    user['show_profile'] = bool(res[4])
    user['show_report'] = bool(res[5])
    user['nickname'] = res[6]
    user['squad'] = res[7] if res[7] is not None else fraction
    user['practice'] = res[8]
    user['theory'] = res[9]
    user['guile'] = res[10]
    user['wisdom'] = res[11]
    if bool(res[3]):
        user['date_report'] = str(res[12])
        user['income'] = res[13]
        user['pure_income'] = res[14]
        user['target'] = res[15]

    return user


def del_user(user_id):
    """
    Delete user from all 3 tables in view vUser
    :param user_id: int, user id from vk [from_id]
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'DELETE FROM tReports WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()
    query = 'DELETE FROM tProfile WHERE cIdUser = %s;'
    cursor.execute(query, data)
    db.commit()
    query = 'DELETE FROM tPreferences WHERE cIdUser = %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def count_role(role_id):
    """
    Count users with selected role in DB
    :param role_id: int, in range of role types count (use get_roles() to check)
    :return: int, count of users with role, int
    """
    if type(role_id) != int:
        try:
            role_id = int(role_id)
        except ValueError:
            raise TypeError("Role Id should be int type")
    elif role_id < 0 or role_id > 13:
        raise ValueError("Role Id should be positive and less or equal 13")

    query = 'SELECT COUNT(*) FROM vUser WHERE cIdRole = %s;'

    db, cursor = db_open()

    cursor.execute(query, (role_id,))
    res = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return res


def set_role(user_id, role_id):
    """
    Write new role to user. Re-write value without checking
    :param user_id: int, user id from vk [from_id]
    :param role_id: int, in range of role types count (use get_roles() to check)
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(role_id) != int:
        try:
            role_id = int(role_id)
        except ValueError:
            raise TypeError("Role Id should be int type")
    if role_id < 0 or role_id > 13:
        raise ValueError("Role Id must be in 0-13")

    data = (role_id, user_id)
    query = 'UPDATE tPreferences SET cIdRole = %s WHERE cIdUser = %s'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_roles():
    """
    Get list of all roles in DB
    :return: list [%role_id%. %role_name%]
    """
    roles = list()
    query = 'SELECT * FROM tRole;'

    db, cursor = db_open()

    cursor.execute(query)
    res = cursor.fetchall()

    db_close(db, cursor)

    for r in res:
        roles.append(str(r[0]) + '. ' + r[1])
    return roles


def get_role(user_id):
    """
    Get user's role from DB
    :param user_id: int, user id from vk [from_id]
    :return: int, role id
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT cIdRole FROM vUser WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        return 13
    else:
        return res[0][0]


def get_preferences(user_id):
    """
    Short version of get_user(), get info about user's preferences from DB
    :param user_id: int, user id from vk [from_id]
    :return: dict {user_id: int, role: int,
    subscribe: bool, report: bool, show_profile: bool, show_report: bool,
    last_message: int}
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM vUser WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        raise ValueError("User doesn't exist, try to reg him first")
    res = res[0]

    user = dict()
    user['user_id'] = res[0]
    user['role'] = res[1]
    user['subscribe'] = bool(res[2])
    user['report'] = bool(res[3])
    user['show_profile'] = bool(res[4])
    user['show_report'] = bool(res[5])
    user['last_message'] = res[6]
    return user


def get_msg(user_id):
    """
    Get user's last time of message from DB
    :param user_id: int, user id from vk [from_id]
    :return: None / int, unix time of message [date]
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'SELECT cLastMsg FROM tPreferences WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        return None
    else:
        return res[0][0]


def update_msg(user_id, msg_time):
    """
    Write new time of last message into DB
    :param user_id: int, user id from vk [from_id]
    :param msg_time: int, unix time from vk [date]
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    try:
        get_user(user_id)
    except ValueError as error:
        raise error

    if type(msg_time) != int:
        try:
            msg_time = int(msg_time)
        except ValueError:
            raise TypeError("Time should be int type")
    elif msg_time > int(time.time()):
        raise ValueError("Time should have lesser value than now (unix)")

    data = (msg_time, user_id)
    query = 'UPDATE tPreferences SET cLastMsg = %s WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def change_preference(user_id, preference):
    """
    Toggles preference in DB
    :param user_id: int, user id from vk [from_id]
    :param preference: str, ['cIsSubscribed', 'cIsReported', 'cShowProfile', 'cShowReport']
    :return: None
    """
    columns = get_columns('tPreferences')[2:-1]

    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(preference) != str:
        try:
            preference = str(preference)
        except ValueError:
            raise TypeError("Preference should be str type")
    if preference not in columns:
        raise ValueError("There is no option \'"+preference+"\'")

    state = get_preference(user_id, preference)
    query = 'UPDATE tPreferences' \
            ' SET ' + preference + ' = ' + str(not state).upper() + \
            ' WHERE cIdUser = ' + str(user_id) + ';'

    db, cursor = db_open()

    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def get_preference(user_id, preference):
    """
    Get state of preference from DB
    :param user_id: int, user id from vk [from_id]
    :param preference: str, ['cissubscribed', 'cisreported', 'cshowprofile', 'cshowreport']
    :return: bool
    """
    columns = get_columns('tPreferences')[2:-1]

    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(preference) != str:
        try:
            preference = str(preference)
        except ValueError:
            raise TypeError("Preference should be str type")
    if preference not in columns:
        raise ValueError("There is no option \'" + preference + "\'")

    query = 'SELECT ' + preference + ' FROM vUser WHERE cIdUser = ' + str(user_id) + ';'

    db, cursor = db_open()

    cursor.execute(query)
    state = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return bool(state)


def get_squad(user_id):
    """
    Get user's squad from DB
    :param user_id: int, user id from vk [from_id]
    :return: str, squad source
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'SELECT cSquad FROM vUser WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    res = cursor.fetchall()

    db_close(db, cursor)
    return res[0][0]


def set_profile(user_id, nick, source, practice, theory, guile, wisdom):
    """
    Write profile data in DB
    :param user_id: int, user id from vk [from_id]
    :param nick: str, user's nickname
    :param source: str, squad initials
    :param practice: int
    :param theory: int
    :param guile: int
    :param wisdom: int
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(nick) != str:
        try:
            nick = str(nick)
        except ValueError:
            raise TypeError("Nickname must be str type")

    if source is not None:
        if type(source) != str:
            try:
                source = str(source)
            except ValueError:
                raise TypeError("Source should be str type")
        elif len(source) > 2:
            raise ValueError("Source length should be less or equal 2")
        source = source.upper()

        if source not in get_squads():
            raise ValueError("There is no squad \"" + source + "\". Try to reg squad first")

    if type(practice) != int:
        try:
            practice = int(practice)
        except ValueError:
            raise TypeError("Practice should be int type")
    elif practice < 0:
        raise ValueError("Practice should be positive")
    if type(theory) != int:
        try:
            theory = int(theory)
        except ValueError:
            raise TypeError("Theory should be int type")
    elif theory < 0:
        raise ValueError("Theory should be positive")
    if type(guile) != int:
        try:
            guile = int(guile)
        except ValueError:
            raise TypeError("Guile should be int type")
    elif guile < 0:
        raise ValueError("Guile should be positive")
    if type(wisdom) != int:
        try:
            wisdom = int(wisdom)
        except ValueError:
            raise TypeError("Wisdom should be int type")
    elif wisdom < 0:
        raise ValueError("Wisdom should be positive")

    data = {'user_id': user_id, 'nick': nick, 'source': source,
            'practice': practice, 'teo': theory, 'hit': guile, 'mud': wisdom}

    query = 'SELECT * FROM tProfile WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    if len(cursor.fetchall()) == 0:
        query = 'INSERT INTO tProfile VALUE(%(user_id)s,%(nick)s,%(source)s,%(practice)s,%(teo)s,%(hit)s,%(mud)s);'
    else:
        query = 'UPDATE tProfile ' \
                'SET cNickname = %(nick)s, cSquad = %(source)s, ' \
                'cPractice = %(practice)s, cTheory = %(teo)s, cGuile = %(hit)s, cWisdom = %(mud)s ' \
                'WHERE cIdUser = %(user_id)s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_profile(user_id):
    """
    Short version of get_user(), get user's profile from DB
    :param user_id: int, user id from vk [from_id]
    :return: dict {user_id: int, nickname: str, squad: str,
    practice: int, theory: int, guile: int, wisdom: int}
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT cIdUser, cNickname, cSquad, cPractice, cTheory, cGuile, cWisdom ' \
            'FROM vUser WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()[0]

    db_close(db, cursor)

    user = dict()
    user['user_id'] = res[0]
    user['nickname'] = res[1]
    user['squad'] = res[2]
    user['practice'] = res[3]
    user['theory'] = res[4]
    user['guile'] = res[5]
    user['wisdom'] = res[6]
    return user


def set_report(user_id, date_rep, income, pure_income, target):
    """
    Writes battle report data in DB
    :param user_id: int, user id from vk [from_id]
    :param date_rep: datetime.date
    :param income: int
    :param pure_income: int, can't be greater of income
    :param target: int, from 0 to 7
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(date_rep) != datetime.date:
        try:
            date_rep = date_rep.date()
        except AttributeError:
            raise TypeError("Date should be datetime.date type")
    elif date_rep > datetime.date.today():
        raise ValueError("Date should have smaller value than today (unix)")

    if type(income) != int:
        try:
            income = int(income)
        except ValueError:
            raise TypeError("Income should be int type")
    if type(pure_income) != int:
        try:
            pure_income = int(pure_income)
        except ValueError:
            raise TypeError("Pure income should be int type")
    if pure_income > income:
        raise ValueError("Pure income can't be bigger than overall income")

    if type(target) != int:
        try:
            target = int(target)
        except ValueError:
            raise TypeError("Target should be int type")
    elif target == fraction or target < 0 or target > 7:
        raise ValueError("Target should have positive value less than 8 and not your fraction itself")

    data = {'user_id': user_id, 'date': date_rep, 'income': income, 'pure_income': pure_income, 'target': target}

    query = 'SELECT * FROM tReports WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    if len(cursor.fetchall()) == 0:
        query = 'INSERT INTO tReports VALUE(%(user_id)s, %(date)s, %(income)s, %(pure_income)s, %(target)s);'
    else:
        query = 'UPDATE tReports ' \
                'SET cDateReport = %(date)s, cIncome = %(income)s, cPureIncome = %(pure_income)s, cTarget = %(target)s ' \
                'WHERE cIdUser = %(user_id)s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)

    change_preference(user_id, 'cIsReported')

    return


def get_report(user_id):
    """
    Get battle report data from DB
    :param user_id: int, user id from vk [from_id]
    :return: dict {user_id: int, date: str(datetime), income: int, pure_income: int, target: int}
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM tReports WHERE cIdUser = %s;'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        raise ValueError("Report doesn't exist, try to add it first")
    res = res[0]

    report = dict()
    report['user_id'] = res[0]
    report['date'] = str(res[1])
    report['income'] = res[2]
    report['pure_income'] = res[3]
    report['target'] = res[4]
    return report


def set_discipline(user_get, user_set, reason, date):
    """
    Add warn for user into DB
    :param user_get: int, user id from vk [from_id]. That user get warn
    :param user_set: int, user id from vk [from_id]. That user set warn
    :param reason: str, reason of warn
    :param date: int, unix timestamp (rework to datetime)
    :return: None
    """
    if type(user_get) != int or type(user_set) != int:
        try:
            user_get = int(user_get)
            user_set = int(user_set)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_get < 0 or user_get >= 2000000000 or user_set < 0 or user_set >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(reason) != str:
        try:
            reason = str(reason)
        except ValueError:
            raise TypeError("Reason should be str type")
    elif len(reason) > 100:
        raise ValueError("Reason should be less or equal 100 symbols")

    if type(date) != int:
        try:
            date = int(date)
        except ValueError:
            raise TypeError("Time should be int type")
    elif date <= int(time.time()):
        raise ValueError("Time should have greater value than now (unix)")

    data = (user_get, user_set, reason, date)
    query = 'INSERT INTO tDiscipline VALUE (%s, %s, %s, %s);'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_discipline(user_id):
    """
    Get all user's warns from DB
    :param user_id: int, user id from vk [from_id]
    :return: list [ dict {from: int, reason: str, time: int(rework for datetime)} ]
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM tDiscipline WHERE cIdUser = %s'

    db, cursor = db_open()

    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        discipline = None
    else:
        discipline = list()
        for i in res:
            warn = dict()
            warn['from'] = i[1]
            warn['reason'] = i[2]
            warn['time'] = i[3]
            discipline.append(warn)
    return discipline


def del_discipline(user_id, count=1):
    """
    Delete warns from user in DB
    :param user_id: int, user id from vk [from_id]
    :param count: int, default 1, can be greater then count of warns
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(count) != int:
        try:
            count = int(count)
        except ValueError:
            raise TypeError("Number should be int type")
    elif count < 0:
        raise ValueError("Number should be positive")

    data = (user_id, count)
    query = 'DELETE FROM tDiscipline WHERE cIdUser = %s LIMIT %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def set_data(user_id, tag, text):
    """
    Write new note into DB
    :param user_id: int, user id from vk [from_id]
    :param tag: str, short tag for search
    :param text: str, text to save
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(tag) != str:
        try:
            tag = str(tag)
        except ValueError:
            raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")
    if get_data(user_id, tag) is not None:
        raise NameError("You already have text with tag \"" + tag + "\"")

    if type(text) != str:
        try:
            text = str(text)
        except ValueError:
            raise TypeError("Text should be str type")

    data = (user_id, tag, text)
    query = 'INSERT INTO tData VALUE (%s, %s, %s);'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_data(user_id, tag):
    """
    Get note by tag from DB
    :param user_id: int, user id from vk [from_id]
    :param tag: str, short tag for search
    :return: None / text by user/tag
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(tag) != str:
        try:
            tag = str(tag)
        except ValueError:
            raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")

    data = (user_id, tag)
    query = 'SELECT * FROM tData WHERE cIdUser = %s AND cTag = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        result = None
    else:
        result = res[0][2]

    return result


def del_data(user_id, tag):
    """
    Delete note by tag from DB
    :param user_id: int, user id from vk [from_id]
    :param tag: str, short tag for search
    :return: None
    """
    if type(user_id) != int:
        try:
            user_id = int(user_id)
        except ValueError:
            raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(tag) != str:
        try:
            tag = str(tag)
        except ValueError:
            raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")

    if get_data(user_id, tag) is None:
        raise NameError("Tag \"" + tag + "\" doesn't exist")

    data = (user_id, tag)
    query = 'DELETE FROM tData WHERE cIdUser = %s AND cTag = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return
