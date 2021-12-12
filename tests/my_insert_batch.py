from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':
    Database.connect(**db)

    User.truncate()

    # 批量插入
    fields = ('name', 'phone', 'money')
    values = [
        ('jack', '18976643333', 120),
        ('sean', '18976654444', 160),
        ('vera', '18976645555', 180),
    ]

    User.insert(fields, values)
