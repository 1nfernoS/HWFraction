from db.db_sql import db_open, db_close
from settings import fraction
import time


def get_token(source):
    db, cursor = db_open()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source length should be less or equal 2 symbols")
    source = source.upper()

    data = (source,)
    query = 'SELECT cToken FROM tSquads WHERE cSource = %s;'
    cursor.execute(query, data)

    res = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return res


def get_squads():
    db, cursor = db_open()

    squads = list()
    query = 'SELECT cSource FROM tSquads;'
    cursor.execute(query)

    for i in cursor.fetchall():
        squads.append(i[0])

    db_close(db, cursor)
    return squads


def count_squads():
    db, cursor = db_open()

    query = 'SELECT COUNT(*) FROM tSquads;'
    cursor.execute(query)
    res = cursor.fetchall()[0][0]

    db_close(db, cursor)
    return res


def reg_squad(source, token):
    db, cursor = db_open()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2 symbols")
    source = source.upper()

    if type(token) != str:
        raise TypeError("Token should be str type")
    elif len(token) != 128:
        raise ValueError("Token's length should be equal 128")

    query = 'SELECT cSource FROM tSquads WHERE cSource = %s;'
    cursor.execute(query, (source,))
    if len(cursor.fetchall()) == 0:
        data = (source, token)
        query = 'INSERT INTO tSquads (cSource, cToken) VALUE (%s, %s);'
    else:
        data = (token, source)
        query = 'UPDATE tSquads SET cToken = %s WHERE cSource = %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def set_chat(source, id_chat):
    db, cursor = db_open()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2 symbols")
    source = source.upper()

    query = 'SELECT * FROM tSquads WHERE cSource = %s;'
    cursor.execute(query, (source,))
    if len(cursor.fetchall()) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    if type(id_chat) != int:
        raise TypeError("Chat Id should be int type")
    elif 0 > id_chat > 2000000000:
        raise ValueError("Chat Id should have positive value less than 2000000000")

    data = (id_chat, source)
    query = 'UPDATE tSquads SET cIdChat = %s WHERE cSource = %s;'
    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def get_leaders(source):
    db, cursor = db_open()

    leaders = list()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2")
    source = source.upper()

    data = (source,)
    query = 'SELECT cIdUser FROM vUser ' \
            'WHERE cSquad = %s AND (cIdRole = 0 OR cIdRole = 1 OR cIdRole = 3 OR cIdRole = 5 OR cIdRole = 7);'
    cursor.execute(query, data)

    for i in cursor.fetchall():
        leaders.append(i[0])

    db_close(db, cursor)
    return leaders


def squad_users(source):
    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2")
    source = source.upper()

    user_list = dict()
    query = 'SELECT cIdUser, cNickname FROM vUser WHERE cSquad = %s;'

    db, cursor = db_open()

    cursor.execute(query, (source,))
    res = cursor.fetchall()

    db_close(db, cursor)

    for i in res:
        user_list[i[0]] = i[1]

    return user_list


def set_target(source, target, timer):
    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2")
    source = source.upper()

    query = 'SELECT * FROM tSquads WHERE cSource = %s;'

    db, cursor = db_open()

    cursor.execute(query, (source,))
    res = cursor.fetchall()

    db_close(db, cursor)

    if len(res) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    if type(target) != int:
        raise TypeError("Target should be int type")
    elif target == fraction or target < 0 or target > 7:
        raise ValueError("Target should have positive value less than 8 and not your fraction itself")

    if type(timer) != int:
        raise TypeError("Time should be int type")
    elif timer < int(time.time()):
        raise ValueError("Time should have greater value than now (unix)")

    data = (target, timer, source)
    query = 'UPDATE tSquads SET cTarget = %s, cTime = %s WHERE cSource = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return


def del_squad(source):
    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2 symbols")
    source = source.upper()

    data = (source,)
    query = 'DELETE FROM tSquads WHERE cSource = %s;'

    db, cursor = db_open()

    cursor.execute(query, data)
    db.commit()

    db_close(db, cursor)
    return
