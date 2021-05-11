"""
This is main connector to database. Main functions are db_open and db_close.
But there is some useful functions if you want to add some functions and you need to work with database.
(c) Misden a.k.a. 1nfernos, 2021
"""
import mysql.connector as sql
from settings import db_data


class DB(object):
    """
    Object of connection to DB. Have single instance for avoid multiple connections
    """
    _connection = sql.connect(user=db_data['user'], password=db_data['password'],
                              host=db_data['host'], database=db_data['database'])

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(DB, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

    def connect(self):
        if not self._connection.is_connected():
            self._connection = sql.connect(user=db_data['user'], password=db_data['password'],
                                           host=db_data['host'], database=db_data['database'])
        return self._connection


def db_open():
    """
    "Open" connection for use DB
    :return: connection, cursor
    """
    db = DB()
    con = db.connect()
    cursor = con.cursor()
    return con, cursor


def db_close(db, cursor):
    """
    "Close" connection for DB
    :param db: connection
    :param cursor: cursor
    :return: None
    """
    cursor.close()
    return


def get_tables():
    """
    Get list of all tables in DB
    :return: list [ %table_name%: str ]
    """
    db, cursor = db_open()

    tables = list()
    query = 'SHOW TABLES;'
    cursor.execute(query)

    for r in cursor.fetchall():
        tables.append(r[0])

    db_close(db, cursor)
    return tables


def get_columns(table):
    """
    Get list of columns from table in DB
    :param table: str, table name (use get_tables() ti check)
    :return: list [ %column_name%: str]
    """
    db, cursor = db_open()

    if str(table).lower() not in get_tables():
        raise NameError("The table '" + table + "' doesn't exists!")

    columns = list()
    query = 'SELECT COLUMN_NAME ' \
            'FROM INFORMATION_SCHEMA.COLUMNS ' \
            'WHERE TABLE_SCHEMA = \'' + db_data['database'] + \
            '\' AND TABLE_NAME = \'' + table + '\' ORDER BY ORDINAL_POSITION;'
    cursor.execute(query)

    for r in cursor.fetchall():
        columns.append(r[0].lower())

    db_close(db, cursor)
    return columns


def get_column_types(table):
    """
    Get structure info about table in DB
    :param table: str, table name (use get_tables() ti check)
    :return: dict { %column_name%: str : %data_type%: str}
    """
    db, cursor = db_open()

    if str(table).lower() not in get_tables():
        raise NameError("The table '" + table + "' doesn't exists!")

    columns = dict()
    query = 'SELECT COLUMN_NAME, COLUMN_TYPE ' \
            'FROM INFORMATION_SCHEMA.COLUMNS ' \
            'WHERE TABLE_SCHEMA = \'' + db_data['database'] + \
            '\' AND TABLE_NAME = \'' + table + '\' ORDER BY ORDINAL_POSITION;'

    cursor.execute(query)

    for r in cursor.fetchall():
        columns[r[0]] = str(r[1].decode('utf-8'))

    db_close(db, cursor)
    return columns


# TODO: Remove after tests
def execute(query):
    """
    Execute query directly into DB
    !!! [DANGER] !!! Use it only if you 101% sure what are you doing
    :param query: str, SQL query
    :return: 'Success' / raw tuple from SELECT statement
    """
    db, cursor = db_open()
    try:
        cursor.execute(query)
        answer = cursor.fetchall()
        db.commit()
    except:
        return
    finally:
        db_close(db, cursor)
    if len(answer) != 0:
        res = list()
        for i in answer:
            res.append(i)
    else:
        res = 'Success'
    return res
