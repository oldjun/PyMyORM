from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

count = User.find().where(status='0').count('id')
print(count)
