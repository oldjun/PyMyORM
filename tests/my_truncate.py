from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)

User.find().truncate()
