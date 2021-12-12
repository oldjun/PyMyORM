from pymyorm.database import Database
from tests.config import db
from tests.models.user import User


if __name__ == '__main__':

    Database().connect(**db)

    money = User.find().where(id=1).scalar('money')
    print(money)
