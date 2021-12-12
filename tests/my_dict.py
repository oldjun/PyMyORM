from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    # # case 1
    # one = User.find().where(name='ping').one()
    # print(one)

    # case 2
    all = User.find().all(raw=True)
    print(all)
