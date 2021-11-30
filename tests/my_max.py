from pymyorm.database import Database
from config import db
from models.user import User


def main():

    Database().connect(**db)

    money = User.find().where(status=0).max('money')
    print(money)


if __name__ == '__main__':
    main()
