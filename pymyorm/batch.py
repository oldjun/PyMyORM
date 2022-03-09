import datetime
import decimal


class Batch(object):

    def __init__(self, cursor):
        self.__cursor = cursor
        self.__raw = False
        self.__size = 0
        self.__left = 0
        self.__model = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.__left <= 0:
            raise StopIteration

        all = self.__cursor.fetchmany(self.__size)
        self.__left -= self.__size
        for one in all:
            for k, v in one.items():
                if isinstance(v, datetime.datetime):
                    one[k] = v.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(v, datetime.date):
                    one[k] = v.strftime('%Y-%m-%d')
                elif isinstance(v, decimal.Decimal):
                    one[k] = float(v)

        if self.__raw:
            return all

        res = []
        for one in all:
            item = self.__model.__class__()
            for (k, v) in one.items():
                item._Model__old_fields[k] = v
            res.append(item)
        return res

    def raw(self, raw):
        self.__raw = raw

    def size(self, size):
        self.__size = size

    def total(self, total):
        self.__left = total

    def model(self, model):
        self.__model = model
