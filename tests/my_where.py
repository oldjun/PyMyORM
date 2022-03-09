from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    name = 'jack'
    status = 1
    where = "name='%s' or status=%s" % (name, status)
    # where2 = f"name='{name}' or status={status}"
    print(where)
    one = User.find().where("name='%s' or status=%s" % (name, status)).one()
    print(one)

    User.find().where("name='%s' or status=%s" % (name, status)).update(status=1)
