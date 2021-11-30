from pymyorm.database import Database
from pymyorm.transaction import Transaction as t
from config import db
from models.user import User

Database().connect(**db)

def create_user():
    fp = open('user.txt', 'r')
    try:
        User.find().truncate()
        t.begin()
        for line in fp:
            line = line.strip('\r\n')
            name, phone, money = line.split()
            model = User()
            model.name = name
            model.phone = phone
            model.money = money
            model.save()
        t.commit()
    except Exception as e:
        t.rollback()
        raise e
    fp.close()

def update_user():
    try:
        t.begin()
        User.find().where(name='ping').update(money=0)
        t.commit()
    except Exception as e:
        t.rollback()
        raise e


def main():
    try:
        t.begin()
        create_user()
        update_user()
        t.commit()
    except Exception as e:
        t.rollback()
        raise e


if __name__ == '__main__':
    main()
