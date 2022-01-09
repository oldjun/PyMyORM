from pymyorm.local import local
from pymyorm.connection import Connection
import os


class Database(object):

    @staticmethod
    def connect(host, port, user, password, database, charset='utf8', debug=False):
        conn = Connection(host=host, port=port, user=user, password=password, database=database, charset=charset)
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
    def model(table, model):
        file = model.split('/')[-1]
        file = file.split('.')[0]
        cls = ''.join([word.capitalize() for word in file.split('_')])
        str = f"from pymyorm.model import Model\n\n\n"
        str += f"class {cls}(Model):\n"
        str += f"\ttablename = '{table}'\n"
        datetime_fields = []
        decimal_fields = []

        all = Database.schema(table)
        for one in all:
            if one['column_key'] == 'PRI':
                if one['column_name'] != 'id':
                    str += f"\tprimary_key = '{one['column_name']}'\n"
            if one['data_type'] == 'timestamp':
                datetime_fields.append(one['column_name'])
            if one['data_type'] == 'decimal':
                decimal_fields.append(one['column_name'])
        if datetime_fields:
            datetime_fields_str = ','.join([f"'{fields}'" for fields in datetime_fields])
            str += f"\tdatetime_fields = [{datetime_fields_str}]\n"
        if decimal_fields:
            decimal_fields_str = ','.join([f"'{fields}'" for fields in decimal_fields])
            str += f"\tdecimal_fields = [{decimal_fields_str}]\n"

        filename = os.path.join(os.getcwd(), model)
        path = os.path.dirname(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        fp = open(filename, 'w', encoding='utf8')
        fp.write(str)
        fp.close()
