from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':
    Database.connect(**db)

    User.truncate()

    fields = ('name', 'phone', 'money', 'gender')
    values = [
        ('ping', '18976641111', 100, 1),
        ('lucy', '18976642222', 100, 2),
        ('lily', '18976643333', 200, 2),
        ('jack', '18976644444', 300, 1),
        ('sean', '18976645555', 500, 1),
        ('vera', '18976646666', 100, 2),
    ]
    User.insert(fields, values)
