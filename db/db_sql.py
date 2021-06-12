"""
This is main connector to database. Main functions are db_open and db_close.
But there is some useful functions if you want to add some functions and you need to work with database.
(c) Misden a.k.a. 1nfernos, 2021
"""
import traceback
import mysql.connector as sql

from vk_api import error
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


def query(operation, *args):
    if args:
        if type(args[0]) == tuple:
            args = args[0]
    db = DB()
    connection = db.connect()
    cursor = connection.cursor()
    try:
        cursor.execute(operation, args)
        res = cursor.fetchall()
        connection.commit()
    except sql.errors.ProgrammingError:
        error('\nERROR\t!!!!!\tERROR\t!!!!!\tERROR\n\n' + str(traceback.format_exc(0)))
        res = None
    except:
        error(traceback.format_exc())
        res = None
    finally:
        cursor.close()
    return res
