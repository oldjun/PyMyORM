from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':

    Database.connect(**db)

    # # case 1
    # user = User(name='rose', phone='18976649999', money=100)
    # user.save()

    # case 2
    user = User()
    user.name = 'vera333'
    user.phone = '18976649999'
    user.money = 100
    user.save()
