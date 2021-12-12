from pymyorm.database import Database
from config import db
from models.user import User


if __name__ == '__main__':
    Database().connect(**db)

    User.truncate()

    fields = ('name', 'phone', 'money', 'gender')
    values = []
    fp = open('user.txt', 'r')
    for line in fp:
        line = line.strip('\r\n')
        value = (name, phone, money, gender) = line.split()
        values.append(value)
    fp.close()

    User.insert(fields, values)
