from demos.config import db
from pymyorm.database import Database
from pymyorm.transaction import Transaction as t
from demos.models.user import User

Database().connect(**db)


def create_user():
    t.begin()
    create_user_inner('ping')
    create_user_inner('lucy', False)
    create_user_inner('lily', False)
    create_user_inner('jack')
    t.commit()


def create_user_inner(name, success=True):
    try:
        t.begin()
        user = User()
        user.name = name
        user.save()
        create_user_inner_deep(f"{name}-inner-001")
        create_user_inner_deep(f"{name}-inner-002", False)
        create_user_inner_deep(f"{name}-inner-003", False)
        create_user_inner_deep(f"{name}-inner-004")
        if success:
            t.commit()
        else:
            t.rollback()
    except Exception as e:
        t.rollback()
        raise e


def create_user_inner_deep(name, success=True):
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


create_user()
