"""
This is main connector to database. Main functions are db_open and db_close.
But there is some useful functions if you want to add some functions and you need to work with database.
(c) Misden a.k.a. 1nfernos, 2021
"""
import mysql.connector as sql
from settings import db_data


# TODO: Make db static class
def db_open():
    db = sql.connect(user=db_data['user'], password=db_data['password'], host=db_data['host'],
                     database=db_data['database'])
    cursor = db.cursor()
    return db, cursor


def db_close(db, cursor):
    db.close()
    cursor.close()
    return


def get_tables():
    db, cursor = db_open()

    tables = list()
    query = 'SHOW TABLES;'
    cursor.execute(query)

    for r in cursor.fetchall():
        tables.append(r[0])

    db_close(db, cursor)
    return tables


def get_columns(table):
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
        columns.append(r[0])

    db_close(db, cursor)
    return columns


def get_column_types(table):
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

