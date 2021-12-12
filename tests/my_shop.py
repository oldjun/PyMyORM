from pymyorm.database import Database
from config import db
from models.shop import Shop


def init():
    Shop.truncate()
    fp = open('shop.txt', 'r')
    for line in fp:
        line = line.strip('\r\n')
        sid, name, phone = line.split()
        model = Shop()
        model.sid = sid
        model.name = name
        model.phone = phone
        model.save()
    fp.close()


if __name__ == '__main__':
    Database.connect(**db)

    # one = Shop.find().where(sid='s-n-1').one()
    # one.name = 'shop-name-x'
    # one.save()
    # print(one)

    Shop.find().where(sid='s-n-1').update(sid='s-n-x')

