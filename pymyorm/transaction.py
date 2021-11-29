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
            num = len(Transaction.__savepoint_list)
            id = f"sp{num}"
            Transaction.__savepoint_list.append(id)
            t.__db.savepoint(id)
        else:
            Transaction.__is_transaction_begin = True
            t.__db.begin()
        # print(Transaction.__savepoint_list)

    @classmethod
    def rollback(cls):
        t = cls()
        num = len(Transaction.__savepoint_list)
        if num > 0:
            id = Transaction.__savepoint_list.pop()
            t.__db.rollback_savepoint(id)
        else:
            t.__db.rollback()
            Transaction.__is_transaction_begin = False
        # print(Transaction.__savepoint_list)

    @classmethod
    def commit(cls):
        t = cls()
        num = len(Transaction.__savepoint_list)
        if num > 0:
            id = Transaction.__savepoint_list.pop()
            t.__db.release_savepoint(id)
        else:
            t.__db.commit()
        # print(Transaction.__savepoint_list)
