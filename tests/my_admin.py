from pymyorm.database import Database
from config import db
from models.admin import Admin
from models.admin_role import AdminRole
from models.admin_auth import AdminAuth


if __name__ == '__main__':

    Database().connect(**db)

    Admin.truncate()
    AdminRole.truncate()
    AdminAuth.truncate()

    for name in ['role1', 'role2', 'role3']:
        exists = AdminRole.find().where(name=name).exists()
        if not exists:
            AdminRole(name=name).save()

    fp = open('admin.txt', 'r')
    for line in fp:
        line = line.strip('\r\n')
        username, phone, password, role, type, lock = line.split()
        model = Admin()
        model.username = username
        model.phone = phone
        model.password = password
        model.role = role
        model.type = type
        model.lock = lock
        model.save()
    fp.close()

    fp = open('admin_auth.txt', 'r')
    for line in fp:
        line = line.strip('\r\n')
        role, action = line.split()
        model = AdminAuth()
        model.role = role
        model.action = action
        model.save()
    fp.close()
