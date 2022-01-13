import pymysql
import time
from pymysql import cursors
from pymyorm.batch import Batch


class Connection(object):

    def __init__(self, host, port, user, password, database, charset='utf8') -> None:
        self.__conn = None
        self.__debug = False
        self.__config = dict(host=host, port=port, user=user, password=password, database=database, charset=charset)
        self.__autocommit = True
        self.__last_ping_time = int(time.time())
        self.__ping = 3600

    def __del__(self):
        self.close()

    def open(self, debug=False):
        self.__debug = debug
        self.close()
        try:
            if self.__debug:
                print(str(self.__config))
            self.__autocommit = True
            self.__conn = pymysql.connect(**self.__config, cursorclass=cursors.DictCursor)
            if self.__debug:
                print('mysql connect success')
        except Exception as e:
            if self.__debug:
                print('mysql connect error')
            raise e

    def close(self):
        if self.__conn is not None:
            if self.__debug:
                print('mysql connection closed')
            self.__conn.close()
            self.__conn = None

    def set_ping(self, seconds):
        self.__ping = seconds

    def ping(self):
        current_time = int(time.time())
        if current_time - self.__last_ping_time > self.__ping:
            try:
                if self.__debug:
                    print('conn ping')
                self.__conn.ping()
            except Exception as e:
                if self.__debug:
                    print(str(e))
        self.__last_ping_time = int(time.time())

    def fetchone(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result
        except pymysql.OperationalError:
            self.open(self.__debug)

    def fetchall(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pymysql.OperationalError:
            self.open(self.__debug)

    def batch(self, sql):
        try:
            if self.__debug:
                print(f"batch sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            return Batch(cursor)
        except pymysql.OperationalError:
            self.open(self.__debug)

    def insert(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            last_insert_id = cursor.lastrowid
            cursor.close()
            return last_insert_id
        except pymysql.OperationalError:
            self.open(self.__debug)

    def insert_batch(self, sql, data):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.executemany(sql, data)
            last_insert_id = cursor.lastrowid
            cursor.close()
            return last_insert_id
        except pymysql.OperationalError:
            self.open(self.__debug)

    def execute(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            num = cursor.execute(sql)
            cursor.close()
            return num
        except pymysql.OperationalError:
            self.open(self.__debug)

    def count(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except pymysql.OperationalError:
            self.open(self.__debug)

    def sum(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except pymysql.OperationalError:
            self.open(self.__debug)

    def min(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except pymysql.OperationalError:
            self.open(self.__debug)

    def max(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except pymysql.OperationalError:
            self.open(self.__debug)

    def average(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total
        except pymysql.OperationalError:
            self.open(self.__debug)

    def exists(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchone()
            total = 0
            for v in data.values():
                total = v
            cursor.close()
            return total == 1
        except pymysql.OperationalError:
            self.open(self.__debug)

    def column(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except pymysql.OperationalError:
            self.open(self.__debug)

    def scalar(self, sql):
        try:
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            self.__conn.autocommit(self.__autocommit)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()
            cursor.close()
            return result
        except pymysql.OperationalError:
            self.open(self.__debug)

    def begin(self):
        try:
            sql = "begin"
            if self.__debug:
                print(f"sql: {sql}")
            if self.__conn is None:
                self.open(self.__debug)
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = False
        except pymysql.OperationalError:
            self.open(self.__debug)

    def rollback(self):
        try:
            sql = "rollback"
            if self.__debug:
                print(f"sql: {sql}")
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = True
        except pymysql.OperationalError:
            self.open(self.__debug)

    def commit(self):
        try:
            sql = "commit"
            if self.__debug:
                print(f"sql: {sql}")
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
            self.__autocommit = True
        except pymysql.OperationalError:
            self.open(self.__debug)

    def savepoint(self, identifier):
        try:
            sql = f"savepoint {identifier}"
            if self.__debug:
                print(f"sql: {sql}")
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except pymysql.OperationalError:
            self.open(self.__debug)

    def rollback_savepoint(self, identifier):
        try:
            sql = f"rollback to savepoint {identifier}"
            if self.__debug:
                print(f"sql: {sql}")
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except pymysql.OperationalError:
            self.open(self.__debug)

    def release_savepoint(self, identifier):
        try:
            sql = f"release savepoint {identifier}"
            if self.__debug:
                print(f"sql: {sql}")
            cursor = self.__conn.cursor()
            cursor.execute(sql)
            cursor.close()
        except pymysql.OperationalError:
            self.open(self.__debug)
