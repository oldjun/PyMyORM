from pymyorm.database import Database
from pymyorm.transaction import Transaction as t
from config import db
from models.user import User


if __name__ == '__main__':

    Database().connect(**db)

    all = User.find().all()
    for one in all:
        try:
            t.begin()
            one.money += 10
            one.save()
            t.commit()
        except Exception as e:
            t.rollback()
            raise e
