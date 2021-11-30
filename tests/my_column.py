from pymyorm.database import Database
from config import db
from models.user import User


def main():

    Database().connect(**db)

    names = User.find().order('id asc').offset(1).limit(2).column('name')
    print(names)


if __name__ == '__main__':
    main()
