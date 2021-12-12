from pymyorm.database import Database
from models.admin_auth import AdminAuth
from config import db


if __name__ == '__main__':
    Database.connect(**db)

    AdminAuth.truncate()

    fields = ['role', 'action']
    values = [
        [1, 'eat'],
        [1, 'drink'],
        [1, 'play'],
        [1, 'happy'],
        [2, 'eat'],
        [2, 'drink'],
        [3, 'eat']
    ]
    AdminAuth.insert(fields, values)
