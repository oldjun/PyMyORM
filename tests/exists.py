from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

exists = User.find().where(name='ping').exists()
print(exists)
