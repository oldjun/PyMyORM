from pymyorm.database import Database
from tests.config import db
from tests.models.user import User


def main():

    Database().connect(**db)

    money = User.find().where(id=1).scalar('money')
    print(money)


if __name__ == '__main__':
    main()
