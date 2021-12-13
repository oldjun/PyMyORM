from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    batch = User.find().batch(size=100)
    for all in batch:
        for one in all:
            print(one)
