import uuid
from pymyorm.local import local


class Transaction(object):

    def __init__(self) -> None:
        print('trx __init__')
        self.__conn = local.conn
        self.__is_transaction_begin = False
        self.__savepoint_list = []

    def __del__(self):
        print('trx __del__')

    @staticmethod
    def begin():
        if not hasattr(local, 'trx'):
            local.trx = Transaction()
        t = local.trx
        print(t)
        # print(Transaction.__is_transaction_begin)
        if t.__is_transaction_begin:
            sp = f"`{str(uuid.uuid4().hex)}`"
            t.__savepoint_list.append(sp)
            t.__conn.savepoint(sp)
        else:
            t.__is_transaction_begin = True
            t.__conn.begin()
        # print(Transaction.__savepoint_list)

    @staticmethod
    def rollback():
        if not hasattr(local, 'trx'):
            local.trx = Transaction()
        t = local.trx
        print(t)
        if len(t.__savepoint_list) > 0:
            sp = t.__savepoint_list.pop()
            t.__conn.rollback_savepoint(sp)
        else:
            t.__conn.rollback()
            t.__is_transaction_begin = False
        # print(Transaction.__savepoint_list)

    @staticmethod
    def commit():
        if not hasattr(local, 'trx'):
            local.trx = Transaction()
        t = local.trx
        print(t)
        if len(t.__savepoint_list) > 0:
            sp = t.__savepoint_list.pop()
            t.__conn.release_savepoint(sp)
        else:
            t.__conn.commit()
            t.__is_transaction_begin = False
        # print(Transaction.__savepoint_list)
