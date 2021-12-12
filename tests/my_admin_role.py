from pymyorm.database import Database
from models.admin_role import AdminRole
from config import db


if __name__ == '__main__':
    Database.connect(**db)

    AdminRole.truncate()

    fields = ['name']
    values = [
        ['role1'],
        ['role2'],
        ['role3']
    ]
    AdminRole.insert(fields, values)
