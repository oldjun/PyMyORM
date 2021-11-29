import pymysql
from pymysql import cursors
from pymyorm.singleton import Singleton


@Singleton
class Database(Singleton):
    def __init__(self) -> None:
        self.__conn = None
        self.__debug = False
        self.__autocommit = True

    def __del__(self):
        if self.__debug:
            print('mysql connection closed')
        if self.__conn is not None:
            self.__conn.close()
            self.__conn = None

    def connect(self, **config):
        try:
            if config.get('debug') is None:
                self.__debug = False
            else:
                self.__debug = config['debug']
                del config['debug']
            if self.__debug:
                print(str(config))
            self.__conn = pymysql.connect(**config, cursorclass=cursors.DictCursor)
            if self.__debug:
                print('mysql connect success')

        except Exception as e:
            if self.__debug:
                print('mysql connect failure')
            raise e

    def fetchone(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            raise e

    def fetchall(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            raise e

    def insert(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            last_insert_id = cursor.lastrowid
            cursor.close()
            return last_insert_id
        except Exception as e:
            raise e

    def execute(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            num = cursor.execute(sql)
            cursor.close()
            return num
        except Exception as e:
            raise e

    def count(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except Exception as e:
            raise e
    
    def min(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except Exception as e:
            raise e

    def max(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except Exception as e:
            raise e

    def average(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except Exception as e:
            raise e

    def exists(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total == 1
        except Exception as e:
            raise e

    def column(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Exception as e:
            raise e

    def scalar(self, sql):
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Exception as e:
            raise e

    def begin(self):
        sql = "begin"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = False
        except Exception as e:
            raise e

    def rollback(self):
        sql = "rollback"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = True
        except Exception as e:
            raise e

    def commit(self):
        sql = "commit"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = True
        except Exception as e:
            raise e

    def savepoint(self, identifier):
        sql = f"savepoint {identifier}"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception as e:
            raise e

    def rollback_savepoint(self, identifier):
        sql = f"rollback to savepoint {identifier}"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception as e:
            raise e
        
    def release_savepoint(self, identifier):
        sql = f"release savepoint {identifier}"
        if self.__debug:
            print(f"sql: {sql}")
        try:
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except Exception as e:
            raise e
