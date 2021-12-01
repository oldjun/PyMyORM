import uuid
from pymyorm.database import Database


class Transaction(object):

    __is_transaction_begin = False
    __savepoint_list = []

    def __init__(self) -> None:
        self.__db = Database()

    @classmethod
    def begin(cls):
        t = cls()
        # print(Transaction.__is_transaction_begin)
        if Transaction.__is_transaction_begin:
            sp = f"{str(uuid.uuid4())}"
            Transaction.__savepoint_list.append(sp)
            t.__db.savepoint(sp)
        else:
            Transaction.__is_transaction_begin = True
            t.__db.begin()
        # print(Transaction.__savepoint_list)

    @classmethod
    def rollback(cls):
        t = cls()
        num = len(Transaction.__savepoint_list)
        if num > 0:
            sp = Transaction.__savepoint_list.pop()
            t.__db.rollback_savepoint(sp)
        else:
            t.__db.rollback()
            Transaction.__is_transaction_begin = False
        # print(Transaction.__savepoint_list)

    @classmethod
    def commit(cls):
        t = cls()
        num = len(Transaction.__savepoint_list)
        if num > 0:
            sp = Transaction.__savepoint_list.pop()
            t.__db.release_savepoint(sp)
        else:
            t.__db.commit()
            Transaction.__is_transaction_begin = False
        # print(Transaction.__savepoint_list)
