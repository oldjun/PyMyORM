from pymyorm.local import local
from pymyorm.connection import Connection


class Database(object):

    @staticmethod
    def connect(host, port, user, password, database, charset='utf8', debug=False):
        conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
        conn.open(debug)
        local.conn = conn

    @staticmethod
    def execute(sql):
        return local.conn.execute(sql)
