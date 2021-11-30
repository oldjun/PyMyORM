#!/usr/bin/env python

from pymyorm.database import Database
from config import db
from models.user import User

Database().connect(**db)


def main():
    print(db)
    # # case 1
    # one = User.find().where(name='ping').one()
    # print(one)

    # # case 2
    # one = User.find().select('name').where(name='ping').where(phone='18976641111').one()
    # print(one)

    # # case 3
    # one = User.find().where(name='ping', phone='18976641111').one()
    # print(one)

    # # case 4
    # one = User.find().where('money', '!=', 200).order('id desc').one()
    # print(one)

    # # case 5
    # all = User.find().where('name', 'not in', ['ping', 'lucy']).all()
    # for one in all:
    #     print(one)

    # # case 6
    # all = User.find().order('id desc').offset(0).limit(5).all()
    # for one in all:
    #     print(one)


if __name__ == '__main__':
    main()
