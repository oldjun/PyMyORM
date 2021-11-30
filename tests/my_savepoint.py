from pymyorm.database import Database
from pymyorm.transaction import Transaction as t
from config import db
from models.user import User

Database().connect(**db)


def main():
    t.begin()
    create_user('ping')
    create_user('lucy', False)
    create_user('lily', False)
    create_user('jack')
    t.commit()


def create_user(name, success=True):
    try:
        t.begin()
        user = User()
        user.name = name
        user.save()
        create_user_inner(f"{name}-inner-001")
        create_user_inner(f"{name}-inner-002", False)
        create_user_inner(f"{name}-inner-003", False)
        create_user_inner(f"{name}-inner-004")
        if success:
            t.commit()
        else:
            t.rollback()
    except Exception as e:
        t.rollback()
        raise e


def create_user_inner(name, success=True):
    try:
        t.begin()
        user = User()
        user.name = name
        user.save()
        if success:
            t.commit()
        else:
            t.rollback()
    except Exception as e:
        t.rollback()
        raise e


if __name__ == '__main__':
    main()
