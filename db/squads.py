from db.db_sql import query

# TODO: delete(?), set chat, set/del remind, set/del target


def reg_squad(source, token):
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("source length more than 2 or empty")

    token = str(token)
    if len(token) != 128:
        raise ValueError("token length is not 128")

    if query('SELECT COUNT(*) FROM t_squad WHERE c_source = %s', source)[0][0] == 0:
        query("INSERT INTO t_squad (c_source, c_token) VALUE %s, %s", source, token)
    else:
        query("UPDATE t_squad, SET c_token = %s WHERE c_source = %s", token, source)
    return


def get_token(source):
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("source length more than 2 or empty")

    if query("SELECT COUNT(*) FROM t_squad WHERE c_source = %s", source)[0] == 0:
        raise ValueError("Unknown squad")

    token = query("SELECT c_token FROM t_squad WHERE c_source = %s", source)[0][0]
    return token


def get_squads():
    res = query("SELECT c_source FROM t_squad;")
    squad_list = list()
    for squad in res:
        squad_list.append(squad[0])
    return squad_list


def change_active(source):
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("source length more than 2 or empty")

    if query("SELECT COUNT(*) FROM t_squad WHERE c_source = %s", source)[0][0] == 0:
        raise ValueError("Unknown squad")

    state = bool(query("SELECT c_is_active FROM t_squad WHERE c_source = %s", source)[0][0])

    query("UPDATE t_squad SET c_is_active = %s WHERE c_source = %s", not state, source)
    return


def set_chat(source, chat_id):
    source = str(source)
    if len(source) > 2 or len(source) == 0:
        raise ValueError("source length more than 2 or empty")

    if query("SELECT COUNT(*) FROM t_squad WHERE c_source = %s", source)[0][0] == 0:
        raise ValueError("Unknown squad")

    try:
        chat_id = int(chat_id)
    except ValueError:
        raise TypeError("chat_id is not int")

    if chat_id < 2000000000:
        raise ValueError("chat_id below 2000000000")

    query("UPDATE t_squad SET c_id_chat = %s WHERE c_source = %s", chat_id, source)
    return

