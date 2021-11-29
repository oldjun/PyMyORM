from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

money = User.find().where(id=1).scalar('money')
print(money)
