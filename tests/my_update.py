from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

# # case 1
# one = User.find().where(name='lily').one()
# one.money = 500
# one.save()

# case 2
User.find().where(name='lily').update(money=180)
