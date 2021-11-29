from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

# case 1
user = User(name='rose', phone='18976645599', money=100)
user.save()

# case 2
user = User()
user.name = 'vera'
user.phone = '18976645599'
user.money = 100
user.save()
