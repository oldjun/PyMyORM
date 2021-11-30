from pymyorm.database import Database
from tests.config import db
from tests.models.user import User

Database().connect(**db)

money = User.find().where(id=1).scalar('money')
print(money)
