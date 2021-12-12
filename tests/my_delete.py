from pymyorm.database import Database
from tests.config import db
from tests.models.user import User


if __name__ == '__main__':

    Database().connect(**db)

    # # case 1
    # one = User.find().where(name='lily').one()
    # one.delete()

    # case 2
    all = User.find().select('name', 'phone').where('money', '>', 100).all()
    for one in all:
        one.delete()

    # # case 3
    # User.find().where(money=100).delete()

    # # case 4
    # User.find().delete()
