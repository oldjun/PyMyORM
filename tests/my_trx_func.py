from pymyorm.transaction import Transaction as t
from models.user import User


def update_user():
    try:
        t.begin()
        User.find().where(name='ping').update(money=0)
        t.commit()
    except Exception as e:
        t.rollback()
        raise e
