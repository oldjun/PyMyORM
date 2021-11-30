from pymyorm.database import Database
from config import db


def main():

    fp = open('sql/t_user.sql', 'r', encoding='utf-8')
    sql = fp.read()
    fp.close()

    d = Database()
    d.connect(**db)
    d.execute(sql)


if __name__ == '__main__':
    main()
