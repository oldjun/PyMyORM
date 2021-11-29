from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

count = User.find().where(status='0').count('id')
print(count)
