from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

User.find().truncate()
