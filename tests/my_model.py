from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)
    Database.model(table='t_user', filename='models/user.py')
