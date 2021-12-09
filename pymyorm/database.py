from pymyorm.local import local
from pymyorm.singleton import Singleton
from pymyorm.connection import Connection


@Singleton
class Database(object):
    def __init__(self) -> None:
        self.__debug = False

    def debug(self, debug=True):
        self.__debug = debug

    def connect(self, host, port, user, password, database, charset='utf8'):
        conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
        conn.open(self.__debug)
        local.conn = conn
