from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

names = User.find().order('id asc').offset(1).limit(2).column('name')
print(names)
