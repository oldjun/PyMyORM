from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

money = User.find().where(status=0).min('money')
print(money)
