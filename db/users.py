import datetime
import time

from settings import fraction
from db.db_sql import db_open, db_close, get_columns
from db.squads import get_squads


def reg_user(user_id, last_msg_time):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(last_msg_time) != int:
        raise TypeError("Time should be int type")
    elif last_msg_time > int(time.time()):
        raise ValueError("Time should have lesser value than now (unix)")

    data = (user_id, last_msg_time)
    query = 'INSERT INTO tPreferences (cIdUser, cIsSubscribed, cIsReported, cShowProfile, cShowReport, cLastMsg) ' \
            'VALUE (%s, FALSE, FALSE, FALSE, FALSE, %s);'
    cursor.execute(query, data)
    db.commit()
    set_profile(user_id, 'Аноним', None, 0, 0, 0, 0)
    set_report(user_id, int(time.time()), 0, 0)

    change_preferences(user_id, 'cIsReported')

    db_close(db, cursor)
    return


def get_user(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM vUser WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()
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

    db_close(db, cursor)
    return user


def del_user(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'DELETE FROM tReports WHERE cIdUser = %s;'
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
    db, cursor = db_open()

    if type(role_id) != int:
        raise TypeError("Role Id should be int type")
    elif role_id < 0 or role_id > 13:
        raise ValueError("Role Id should be positive and less or equal 13")

    query = 'SELECT COUNT(*) FROM tPreferences WHERE cIdRole = %s;'
    cursor.execute(query, (role_id,))
    res = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return res


def set_role(user_id, role):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(role) != int:
        raise TypeError("Role should be int type")
    if role < 0 or role > 13:
        raise ValueError("Role Id must be in 0-13")

    data = (role, user_id)
    query = 'UPDATE tPreferences SET cIdRole = %s WHERE cIdUser = %s'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_roles():
    db, cursor = db_open()

    roles = list()
    query = 'SELECT * FROM tRole'
    cursor.execute(query)

    for r in cursor.fetchall():
        roles.append(str(r[0]) + '. ' + r[1])

    db_close(db, cursor)
    return roles


def get_role(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT cIdRole FROM tPreferences WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()

    db_close(db, cursor)
    if len(res) == 0:
        return 13
    else:
        return res[0][0]


def get_preferences(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM vUser WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()
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

    db_close(db, cursor)
    return user


def get_msg(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'SELECT cLastMsg FROM tPreferences WHERE cIdUser = %s;'
    cursor.execute(query, data)
    res = cursor.fetchall()

    db_close(db, cursor)
    if len(res) == 0:
        return None
    else:
        return res[0][0]


def update_msg(user_id, msg_time):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    try:
        get_user(user_id)
    except ValueError as error:
        raise error

    if type(msg_time) != int:
        raise TypeError("Time should be int type")
    elif msg_time > int(time.time()):
        raise ValueError("Time should have lesser value than now (unix)")

    data = (msg_time, user_id)
    query = 'UPDATE tPreferences SET cLastMsg = %s WHERE cIdUser = %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def change_preferences(user_id, preference):
    db, cursor = db_open()

    columns = get_columns('tPreferences')[2:-1]

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(preference) != str:
        raise TypeError("Preference should be str type")
    if preference not in columns:
        raise ValueError("There is no option \'"+preference+"\'")

    state = get_preference(user_id, preference)
    query = 'UPDATE tPreferences' \
            ' SET ' + preference + ' = ' + str(not state).upper() + \
            ' WHERE cIdUser = ' + str(user_id) + ';'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def get_preference(user_id, preference):
    db, cursor = db_open()

    columns = get_columns('tPreferences')[2:-1]

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(preference) != str:
        raise TypeError("Preference should be str type")
    if preference not in columns:
        raise ValueError("There is no option \'" + preference + "\'")

    query = 'SELECT ' + preference + ' FROM tPreferences WHERE cIdUser = ' + str(user_id) + ';'
    cursor.execute(query)
    state = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return bool(state)


def get_squad(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    data = (user_id,)
    query = 'SELECT cSquad FROM vUser WHERE cIdUser = %s;'
    cursor.execute(query, data)
    res = cursor.fetchall()

    db_close(db, cursor)
    return res[0][0]


def set_profile(user_id, nick, source, practice, theory, guile, wisdom):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(nick) != str:
        raise TypeError("Nickname must be str type")

    if source is not None:
        if type(source) != str:
            raise TypeError("Source should be str type")
        elif len(source) > 2:
            raise ValueError("Source length should be less or equal 2")
        source = source.upper()

        if source not in get_squads():
            raise ValueError("There is no squad \"" + source + "\". Try to reg squad first")

    if type(practice) != int:
        raise TypeError("Practice should be int type")
    elif practice < 0:
        raise ValueError("Practice should be positive")
    if type(theory) != int:
        raise TypeError("Theory should be int type")
    elif theory < 0:
        raise ValueError("Theory should be positive")
    if type(guile) != int:
        raise TypeError("Guile should be int type")
    elif guile < 0:
        raise ValueError("Guile should be positive")
    if type(wisdom) != int:
        raise TypeError("Wisdom should be int type")
    elif wisdom < 0:
        raise ValueError("Wisdom should be positive")

    data = {'user_id': user_id, 'nick': nick, 'source': source,
            'practice': practice, 'teo': theory, 'hit': guile, 'mud': wisdom}

    query = 'SELECT * FROM tProfile WHERE cIdUser = %s;'
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
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM tProfile WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()[0]

    user = dict()
    user['user_id'] = res[0]
    user['nickname'] = res[1]
    user['squad'] = res[2]
    user['practice'] = res[3]
    user['theory'] = res[4]
    user['guile'] = res[5]
    user['wisdom'] = res[6]

    db_close(db, cursor)
    return user


def set_report(user_id, date, income, pure_income):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(date) != int:
        raise TypeError("Time should be int type")
    elif date > int(time.time()):
        raise ValueError("Time should have smaller value than now (unix)")
    date = datetime.date.fromtimestamp(date)

    if type(income) != int:
        raise TypeError("Income should be int type")
    elif income < 0:
        raise ValueError("Income should be positive")
    if type(pure_income) != int:
        raise TypeError("Pure income should be int type")
    elif pure_income < 0:
        raise ValueError("pure income should be positive")

    data = {'user_id': user_id, 'date': date, 'income': income, 'pure_income': pure_income}

    query = 'SELECT * FROM tReports WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    if len(cursor.fetchall()) == 0:
        query = 'INSERT INTO tReports VALUE(%(user_id)s, %(date)s, %(income)s, %(pure_income)s);'
    else:
        query = 'UPDATE tReports ' \
                'SET cDateReport = %(date)s, cIncome = %(income)s, cPureIncome = %(pure_income)s ' \
                'WHERE cIdUser = %(user_id)s;'
    cursor.execute(query, data)
    db.commit()

    change_preferences(user_id, 'cIsReported')

    db_close(db, cursor)
    return


def get_report(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM tReports WHERE cIdUser = %s;'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()
    if len(res) == 0:
        raise ValueError("Report doesn't exist, try to add it first")
    res = res[0]

    report = dict()
    report['user_id'] = res[0]
    report['date'] = str(res[1])
    report['income'] = res[2]
    report['pure_income'] = res[3]

    db_close(db, cursor)
    return report


def set_discipline(user_get, user_set, reason, date):
    db, cursor = db_open()

    if type(user_get) != int or type(user_set) != int:
        raise TypeError("User Id should be int type")
    elif user_get < 0 or user_get >= 2000000000 or user_set < 0 or user_set >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(reason) != str:
        raise TypeError("Reason should be str type")
    elif len(reason) > 100:
        raise ValueError("Reason should be less or equal 100 symbols")

    if type(date) != int:
        raise TypeError("Time should be int type")
    elif date <= int(time.time()):
        raise ValueError("Time should have greater value than now (unix)")

    data = (user_get, user_set, reason, date)
    query = 'INSERT INTO tDiscipline VALUE (%s, %s, %s, %s);'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_discipline(user_id):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    query = 'SELECT * FROM tDiscipline WHERE cIdUser = %s'
    cursor.execute(query, (user_id,))
    res = cursor.fetchall()
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

    db_close(db, cursor)
    return discipline


def del_discipline(user_id, count=1):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(count) != int:
        raise TypeError("Number should be int type")
    elif count < 0:
        raise ValueError("Number should be positive")

    data = (user_id, count)
    query = 'DELETE FROM tDiscipline WHERE cIdUser = %s LIMIT %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def set_data(user_id, tag, text):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(tag) != str:
        raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")
    if get_data(user_id, tag) is not None:
        raise NameError("You already have text with tag \"" + tag + "\"")

    if type(text) != str:
        raise TypeError("Text should be str type")

    data = (user_id, tag, text)
    query = 'INSERT INTO tData VALUE (%s, %s, %s);'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_data(user_id, tag):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")

    if type(tag) != str:
        raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")

    data = (user_id, tag)
    query = 'SELECT * FROM tData WHERE cIdUser = %s AND cTag = %s;'
    cursor.execute(query, data)
    res = cursor.fetchall()
    if len(res) == 0:
        result = None
    else:
        result = res[0][2]

    db_close(db, cursor)
    return result


def del_data(user_id, tag):
    db, cursor = db_open()

    if type(user_id) != int:
        raise TypeError("User Id should be int type")
    elif user_id < 0 or user_id >= 2000000000:
        raise ValueError("User Id should be positive and less than 2000000000")
    if get_data(user_id, tag) is None:
        raise NameError("Tag \"" + tag + "\" doesn't exist")

    if type(tag) != str:
        raise TypeError("Tag should be str type")
    elif len(tag) > 20:
        raise ValueError("Tag's length should be less than 20 symbols")

    data = (user_id, tag)
    query = 'DELETE FROM tData WHERE cIdUser = %s AND cTag = %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return
