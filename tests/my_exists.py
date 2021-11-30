from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

exists = User.find().where(name='ping').exists()
print(exists)
