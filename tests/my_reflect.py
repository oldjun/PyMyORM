from pymyorm.database import Database
from config import db
import os


if __name__ == '__main__':
    Database.connect(**db)
    model = os.path.join(os.getcwd(), 'models/test/test/user.py')
    Database.reflect(table='t_user', model=model)
