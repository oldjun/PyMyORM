from pymyorm.database import Database
from config import db
from models.user import User

if __name__ == '__main__':
    Database.connect(**db)

    # # case 1
    # all = User.find().select('count(*) as count', 'money').group('money').order('count asc').all()
    # for one in all:
    #     print(one)

    all = User.find().select('gender', 'count(*) as count', 'avg(money) as avg').group('gender').all()
    for one in all:
        print(one)
