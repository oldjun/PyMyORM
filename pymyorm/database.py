from pymyorm.local import local
from pymyorm.singleton import Singleton
from pymyorm.connection import Connection


@Singleton
class Database(object):
    def __init__(self) -> None:
        self.__conn = None
        self.__debug = False

    def __del__(self):
        self.close()

    def debug(self, debug=True):
        self.__debug = debug

    def connect(self, host, port, user, password, database, charset='utf8'):
        self.close()
        self.__conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
        self.__conn.open(self.__debug)
        local.conn = self.__conn

    def close(self):
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None
            local.conn = None
