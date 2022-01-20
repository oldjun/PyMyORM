from pymyorm.database import Database
from tests.config import db
from tests.models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    total = User.find().where('brief', 'is', None).count()
    print(total)

    one = User.find().where(name='sean').one()
    one.brief = '123'
    one.save()
