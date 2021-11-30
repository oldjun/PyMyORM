from pymyorm.database import Database
from config import db
from models.user import User


def main():
    Database().connect(**db)

    User.find().truncate()

    fp = open('user.txt', 'r')
    for line in fp:
        line = line.strip('\r\n')
        name, phone, money = line.split()
        model = User()
        model.name = name
        model.phone = phone
        model.money = money
        model.save()
    fp.close()


if __name__ == '__main__':
    main()
