from db.db_sql import db_open, db_close
import time


def get_token(source):
    db, cursor = db_open()

    if type(source) != str or len(source) > 2:
        raise TypeError("Source should be str type and it's length should be less or equal 2")
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

    if type(source) != str or len(source) > 2:
        raise TypeError("Source should be str type and it's length should be less or equal 2")
    source = source.upper()

    if type(token) != str or len(token) != 128:
        raise TypeError("Token should be str type and it's length should be equal 128")

    query = 'INSERT INTO tSquads (cSource, cToken) ' \
            'VALUE (\"' + source + '\", \"' + token + '\");'

    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def set_chat(source, id_chat):
    db, cursor = db_open()

    if type(source) != str or len(source) > 2:
        raise TypeError("Source should be str type and it's length should be less or equal 2")
    source = source.upper()

    query = 'SELECT * FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    if len(cursor.fetchall()) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    if type(id_chat) != int or 0 > id_chat > 2000000000:
        raise TypeError("Chat Id should be int type and have positive value less than 2000000000")

    query = 'UPDATE tSquads SET cIdChat = ' + str(id_chat) + ' WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def set_target(source, target, timer):
    db, cursor = db_open()

    if type(source) != str or len(source) > 2:
        raise TypeError("Source should be str type and it's length should be less or equal 2")
    source = source.upper()

    query = 'SELECT * FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    if len(cursor.fetchall()) == 0:
        raise NameError("There is no \'" + source + "\' squad")

    # TODO: target != fraction itself
    if type(target) != int or target < 0 or target > 7:
        raise TypeError("Target should be int type and have positive value less than 8")

    if type(timer) != int or timer < int(time.time()):
        raise TypeError("Time should be int type, and have greater value than now (unix)")

    query = 'UPDATE tSquads SET cTarget = ' + str(target) + \
            ', cTime = ' + str(timer) + ' WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return


def del_squad(source):
    db, cursor = db_open()

    if type(source) != str or len(source) > 2:
        raise TypeError("Source should be str type and it's length should be less or equal 2")
    source = source.upper()

    query = 'DELETE FROM tSquads WHERE cSource = \"' + source + '\";'
    cursor.execute(query)
    db.commit()

    db_close(db, cursor)
    return
