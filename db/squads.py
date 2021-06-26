import datetime as t

from db.db_sql import query

# TODO: delete(?)


def _validate_source(source):
    """
    Inner method to check source for valid input
    :param source: str, squad's source
    :raise ValueError - incorrect source
    :raise: KeyError - squad doesn't exists in DB
    """
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("Source length more than 2 or empty")
    if query("SELECT COUNT(*) FROM t_squad WHERE c_source = %s", source)[0] == 0:
        raise KeyError("Unknown squad")
    return


def reg_squad(source, token):
    """

    :param source:
    :param token:
    :return:
    """
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("source length more than 2 or empty")

    token = str(token)
    if len(token) != 128:
        raise ValueError("token length is not 128")

    if query('SELECT COUNT(*) FROM t_squad WHERE c_source = %s', source)[0][0] == 0:
        query("INSERT INTO t_squad (c_source, c_token) VALUE %s, %s", source, token)
    else:
        query("UPDATE t_squad SET c_token = %s WHERE c_source = %s", token, source)
    return


def get_token(source):
    _validate_source(source)
    token = query("SELECT c_token FROM t_squad WHERE c_source = %s", source)[0][0]
    return token


def get_squads():
    res = query("SELECT c_source FROM t_squad;")
    squad_list = list()
    for squad in res:
        squad_list.append(squad[0])
    return squad_list


def change_active(source):
    _validate_source(source)

    state = bool(query("SELECT c_is_active FROM t_squad WHERE c_source = %s", source)[0][0])

    query("UPDATE t_squad SET c_is_active = %s WHERE c_source = %s", not state, source)
    return


def set_chat(source, chat_id):
    _validate_source(source)

    try:
        chat_id = int(chat_id)
    except ValueError:
        raise TypeError("chat_id is not int")
    if chat_id < 2000000000:
        raise ValueError("chat_id should be greater than 2000000000")

    query("UPDATE t_squad SET c_id_chat = %s WHERE c_source = %s", chat_id, source)
    return


def set_remind(source, time):
    """
    Updates squad's remind for battle
    :param source: str(2), squad's source
    :param time: datetime.time, time UTC +3 for remind
    :raise TypeError if not datetime.time
    """
    _validate_source(source)

    # time already sent as datetime.time, and we can't parse nor convert, so we just check it
    if type(time) != t.time:
        raise TypeError("Time is not valid type")

    query("UPDATE t_squad SET c_remind_delay = %s WHERE c_source = %s;", time, source)
    return


def del_remind(source):
    """
    Delete remind for battle timer for squad
    :param source: str(2), squad's source
    """
    _validate_source(source)

    query("UPDATE t_squad SET c_remind_delay = NULL WHERE c_source = %s;", source)
    return


def set_target(source, target, time):
    """
    Set target to send in specified time for squad
    :param source: str(2), squad's source
    :param target: int [0-7]
    :param time: datetime.time, time UTC +3 for remind
    :raise ValueError on wrong target
    :raise TypeError on wrong type of target or time
    """
    _validate_source(source)

    if type(target) != int:
        try:
            target = int(target)
        except ValueError:
            raise TypeError("Target is not int")
    if target > 7 or target < 0:
        # no check for fraction because checking only valid data
        raise ValueError("Target must be in [0..7]")

    # time already sent as datetime.time, and we can't parse nor convert, so we just check it
    if type(time) != t.time:
        raise TypeError("Time is not valid type")

    query("UPDATE t_squad SET c_target = %s, c_target_delay = %s WHERE c_source = %s;", target, time, source)
    return


def del_target(source):
    """
    Removes target and delay by squad's source
    :param source: str(2), squad's source
    """
    _validate_source(source)

    query("UPDATE t_squad SET c_target = NULL, c_target_delay = NULL WHERE c_source = %s;", source)
    return

