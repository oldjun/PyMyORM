from demos.config import db
from pymyorm.database import Database
from demos.models.user import User

Database().connect(**db)

User.find().truncate()

fp = open('tests/user.txt', 'r')
for line in fp:
    line = line.strip('\r\n')
    name, phone, money = line.split()
    model = User()
    model.name = name
    model.phone = phone
    model.money = money
    model.save()
fp.close()
