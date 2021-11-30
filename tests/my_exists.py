from pymyorm.database import Database
from config import db
from models.user import User


def main():

    Database().connect(**db)

    exists = User.find().where(name='ping').exists()
    print(exists)


if __name__ == '__main__':
    main()
