from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    # one = User.find().one()
    # print(one)

    all = User.find().all()
    for one in all:
        print(one)
