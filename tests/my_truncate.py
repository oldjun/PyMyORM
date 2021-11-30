from pymyorm.database import Database
from config import db
from models.user import User


def main():

    Database().connect(**db)

    User.find().truncate()


if __name__ == '__main__':
    main()
