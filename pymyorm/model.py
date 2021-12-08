from pymyorm.local import local


class Model(object):
    tablename = None
    primary_key = 'id'

    def __init__(self, **kwargs) -> None:
        self.__conn = local.conn
        self.__sql = ''
        self.__old_fields = {}
        self.__new_fields = {}
        self.__select = []
        self.__update = {}
        self.__where = []
        self.__order = {}
        self.__group = {}
        self.__offset = ''
        self.__limit = ''
        self.__alias = ''
        self.__join = []
        for field, value in kwargs.items():
            self.__new_fields[field] = value

    def __del__(self):
        pass

    def __setattr__(self, name, value):
        if name.find('_Model__') >= 0:
            self.__dict__[name] = value
        else:
            self.__dict__['_Model__new_fields'][name] = value

    def __getattr__(self, name):
        if name in self.__new_fields:
            return self.__new_fields[name]
        elif name in self.__old_fields:
            return self.__old_fields[name]
        else:
            raise Exception(f"object has no attribute '{name}'")

    def __str__(self):
        fields = {}
        fields.update(self.__old_fields)
        fields.update(self.__new_fields)
        return str(fields)

    @classmethod
    def find(cls):
        return cls()

    def save(self):
        if self.__old_fields.get(self.__class__.primary_key) is None:
            fields = ','.join([f"`{item}`" for item in self.__new_fields.keys()])
            values = ','.join([f"'{item}'" for item in self.__new_fields.values()])
            if len(fields) == 0:
                raise Exception('insert fields is empty')
            sql = f"insert into `{self.__class__.tablename}`({fields}) values({values})"
            self.__sql = sql
            last_insert_id = self.__conn.insert(sql)
            self.__new_fields[self.__class__.primary_key] = last_insert_id
        else:
            update_str = ','.join([f"`{k}`='{v}'" for (k, v) in self.__new_fields.items()])
            sql = f"update `{self.__class__.tablename}` set {update_str} where `{self.__class__.primary_key}`='{self.__old_fields.get(self.__class__.primary_key)}'"
            self.__sql = sql
            self.__conn.execute(sql)

    def sql(self):
        sql = self.__build_select_sql()
        if self.__alias:
            sql += f"as `{self.__alias}` "
        sql += self.__build_join_sql()
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__sql

    def __build_select_sql(self):
        sql = f"select "
        if len(self.__select) > 0:
            if self.__alias:
                pk = f"`{self.__alias}`.`{self.primary_key}`"
                if pk not in self.__select:
                    ak = f"`{self.__alias}`.*"
                    if ak not in self.__select:
                        self.__select.insert(0, pk)
            else:
                pk = f"`{self.primary_key}`"
                if pk not in self.__select:
                    if '*' not in self.__select:
                        self.__select.insert(0, pk)
            sql += ','.join([f"{item}" for item in self.__select])
        else:
            sql += "*"
        sql += f" from `{self.__class__.tablename}` "
        return sql

    def __build_where_sql(self):
        sql = ''
        cond_list = []
        for cond in self.__where:
            if cond['op'] in ['=', '!=', '>', '>=', '<', '<=', 'like', 'not like']:
                cond_list.append(f"{cond['field']} {cond['op']} '{cond['value']}'")
            elif cond['op'] in ['in', 'not in']:
                if not isinstance(cond['value'], list):
                    raise Exception('condition in or not in should be a list')
                v_list = []
                for v in cond['value']:
                    v_list.append(f"'{v}'")
                cond_list.append(f"{cond['field']} {cond['op']} ({','.join(v_list)})")
        where_sql = ' and '.join(cond_list)
        if where_sql:
            sql = f"where {where_sql} "
        return sql

    def __build_other_sql(self):
        sql = ''
        if self.__order:
            sql += f"order by {self.__order} "
        if self.__group:
            sql += f"group by {self.__group} "
        if self.__limit:
            if self.__offset:
                sql += f"limit {self.__offset},{self.__limit}"
            else:
                sql += f"limit {self.__limit}"
        return sql

    def __build_join_sql(self):
        sql = ''
        for join in self.__join:
            arr = join['on'].split('=')
            if len(arr) != 2:
                raise Exception(f"syntax error: join on condition {join['on']}")
            field_arr = []
            for field in [one.strip() for one in arr]:
                _arr = field.split('.')
                if len(_arr) != 2:
                    raise Exception(f"syntax error: join on condition {join['on']}")
                field_str = f"`{_arr[0].strip()}`.`{_arr[1].strip()}`"
                field_arr.append(field_str)
            on = '='.join(field_arr)
            sql += f"{join['type']} join `{join['table']}` as `{join['alias']}` on {on} "
        return sql

    def one(self):
        if self.__class__.tablename is None:
            raise Exception('missing table name')

        self.__limit = 1
        sql = self.sql()

        one = self.__class__()
        res = self.__conn.fetchone(sql)
        if res is None:
            return None
        for (k, v) in res.items():
            one.__old_fields[k] = v
        return one

    def all(self):
        if self.__class__.tablename is None:
            raise Exception('missing table name')
        sql = self.sql()
        res = self.__conn.fetchall(sql)
        if res is None:
            return []
        all = []
        for one in res:
            item = self.__class__()
            for (k, v) in one.items():
                item.__old_fields[k] = v
            all.append(item)
        return all

    def alias(self, alias):
        self.__alias = alias
        return self

    def join(self, table, alias, on, type='inner'):
        self.__join.append(dict(table=table, alias=alias, on=on, type=type))
        return self

    def select(self, *args):
        arg_list = []
        for arg in args:
            arg = arg.strip()
            if arg.find('.'):
                temp = []
                for v in arg.split('.'):
                    if v == '*':
                        temp.append(v)
                    else:
                        temp.append(f"`{v}`")
                field = '.'.join(temp)
            else:
                if arg == '*':
                    field = arg
                else:
                    field = f"`{arg}`"
            arg_list.append(field)
        self.__select.extend(arg_list)
        return self

    def update(self, **kwargs):
        if self.__class__.tablename is None:
            raise Exception('missing table name')
        self.__update.update(kwargs)
        sql = f"update `{self.__class__.tablename}` "
        update_str = ','.join([f"`{k}`='{v}'" for (k, v) in self.__update.items()])
        if not update_str:
            raise Exception('missing update statement')
        sql += f"set {update_str} "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__conn.execute(self.__sql)

    def delete(self):
        if self.__class__.tablename is None:
            raise Exception('missing table name')

        sql = f"delete from `{self.__class__.tablename}` "
        if self.__old_fields.get(self.__class__.primary_key) is None:
            sql += self.__build_where_sql()
            sql += self.__build_other_sql()
        else:
            sql += f"where `{self.__class__.primary_key}`='{self.__old_fields.get(self.__class__.primary_key)}'"

        self.__sql = sql.strip()
        return self.__conn.execute(self.__sql)

    def truncate(self):
        if self.__class__.tablename is None:
            raise Exception('missing table name')
        sql = f"truncate table `{self.__class__.tablename}`"
        self.__sql = sql.strip()
        return self.__conn.execute(self.__sql)

    def where(self, *args, **kwargs):
        if len(args) > 0:
            if len(args) != 3:
                raise Exception('where statement error')
            field = args[0]
            if field.find('.'):
                field = '.'.join([f"`{v}`" for v in field.split('.')])
            cond = dict()
            cond['op'] = args[1]
            cond['field'] = field
            cond['value'] = args[2]
            self.__where.append(cond)
        if len(kwargs) > 0:
            for k, v in kwargs.items():
                cond = dict()
                cond['op'] = '='
                cond['field'] = f"`{k}`"
                cond['value'] = v
                self.__where.append(cond)
        return self

    def order(self, order):
        self.__order = order
        return self

    def group(self, group):
        self.__group = group
        return self

    def offset(self, offset):
        self.__offset = offset
        return self

    def limit(self, limit):
        self.__limit = limit
        return self

    def count(self, field=None):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = "select "
        if field is not None:
            if field == '*':
                sql += "count(*) "
            else:
                sql += f"count(`{field}`) "
        else:
            sql += "count(*) "
        sql += f"from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__conn.count(self.__sql)

    def min(self, field):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = f"select min(`{field}`) from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__conn.min(self.__sql)

    def max(self, field):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = f"select max(`{field}`) from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__conn.max(self.__sql)

    def average(self, field):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = f"select avg(`{field}`) from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        return self.__conn.average(self.__sql)

    def exists(self):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = f"select exists(select `{self.__class__.primary_key}` from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        sql = sql.strip()
        sql += f")"
        self.__sql = sql
        return self.__conn.exists(self.__sql)

    def column(self, field):
        if self.__class__.tablename is None:
            raise('missing table name')
        sql = f"select `{field}` from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        result = self.__conn.column(self.__sql)
        return [item[field] for item in result]

    def scalar(self, field):
        if self.__class__.tablename is None:
            raise('missing table name')
        self.__limit = 1
        sql = f"select `{field}` from `{self.__class__.tablename}` "
        sql += self.__build_where_sql()
        sql += self.__build_other_sql()
        self.__sql = sql.strip()
        result = self.__conn.scalar(self.__sql)
        if result is None:
            return None
        return result[field]
