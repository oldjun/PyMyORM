from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)

    table = 't_user'
    exists = Database.exists(table)
    print(exists)
