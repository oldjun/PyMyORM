from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)

    sql = "select * from t_user"
    all = Database.query(sql)
    for one in all:
        print(one)
