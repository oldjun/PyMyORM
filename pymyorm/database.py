from pymyorm.local import local
from pymyorm.connection import Connection
import os


class Database(object):

    @staticmethod
    def connect(host, port, user, password, database, charset='utf8', debug=False, lazy=True):
        conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
        if not lazy:
            conn.open(debug)
        local.conn = conn

    @staticmethod
    def execute(sql):
        return local.conn.execute(sql)

    @staticmethod
    def query(sql):
        return local.conn.fetchall(sql)

    @staticmethod
    def tables():
        database = local.conn._Connection__config['database']
        sql = f"select table_name from information_schema.tables WHERE table_schema='{database}'"
        all = local.conn.fetchall(sql)
        return [one['table_name'] for one in all]

    @staticmethod
    def schema(table):
        database = local.conn._Connection__config['database']
        sql = f"select column_name,column_key,data_type,extra,column_comment from information_schema.columns where table_schema='{database}' and table_name='{table}'"
        return local.conn.fetchall(sql)

    @staticmethod
    def reflect(table, model):
        file = model.split('/')[-1]
        file = file.split('.')[0]
        cls = ''.join([word.capitalize() for word in file.split('_')])
        str = f"from pymyorm.model import Model\n\n\n"
        str += f"class {cls}(Model):\n"
        str += f"\ttablename = '{table}'\n"

        all = Database.schema(table)
        for one in all:
            if one['column_key'] == 'PRI':
                if one['column_name'] != 'id':
                    str += f"\tprimary_key = '{one['column_name']}'\n"

        path = os.path.dirname(model)
        if not os.path.exists(path):
            os.makedirs(path)
        fp = open(model, 'w', encoding='utf8')
        fp.write(str)
        fp.close()
