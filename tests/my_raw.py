from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)
    sql = "update t_user set name='test' where id=1"
    Database.execute(sql)
