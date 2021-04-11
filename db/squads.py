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

    query = 'SELECT cToken FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)

    db_close(db, cursor)
    return cursor.fetchall()[0][0]


def get_squads():
    db, cursor = db_open()

    squads = list()
    query = 'SELECT cSource FROM tSquads;'
    cursor.execute(query)

    for i in cursor.fetchall():
        squads.append(i[0])

    db_close(db, cursor)
    return squads


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

    query = 'INSERT INTO tSquads (cSource, cToken) ' \
            'VALUE (\"' + source + '\", \"' + token + '\");'

    cursor.execute(query)
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

    query = 'SELECT * FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    if len(cursor.fetchall()) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    if type(id_chat) != int:
        raise TypeError("Chat Id should be int type")
    elif 0 > id_chat > 2000000000:
        raise ValueError("Chat Id should have positive value less than 2000000000")

    query = 'UPDATE tSquads SET cIdChat = ' + str(id_chat) + ' WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
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
    query = 'SELECT cIdUser FROM vUser WHERE cSquad = %s AND (cIdRole = 5 OR cIdRole = 4);'
    cursor.execute(query, data)

    for i in cursor.fetchall():
        leaders.append(i[0])

    db_close(db, cursor)
    return leaders


def set_target(source, target, timer):
    db, cursor = db_open()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2")
    source = source.upper()

    query = 'SELECT * FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    if len(cursor.fetchall()) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    if type(target) != int:
        raise TypeError("Target should be int type")
    elif target == fraction or target < 0 or target > 7:
        raise ValueError("Target should have positive value less than 8 and not your fraction itself")

    if type(timer) != int:
        raise TypeError("Time should be int type")
    elif timer < int(time.time()):
        raise ValueError("Time should have greater value than now (unix)")

    query = 'UPDATE tSquads SET cTarget = ' + str(target) + \
            ', cTime = ' + str(timer) + ' WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def del_squad(source):
    db, cursor = db_open()

    if type(source) != str:
        raise TypeError("Source should be str type")
    elif len(source) > 2:
        raise ValueError("Source's length should be less or equal 2 symbols")
    source = source.upper()

    query = 'DELETE FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return
