from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

money = User.find().where(status=0).min('money')
print(money)
