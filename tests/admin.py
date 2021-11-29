from demos.config import db
from pymyorm.database import Database
from demos.models.admin import Admin
from demos.models.admin_role import AdminRole
from demos.models.admin_auth import AdminAuth

Database().connect(**db)

Admin.find().truncate()
AdminRole.find().truncate()
AdminAuth.find().truncate()

for name in ['超级管理员', '运营专员', '客服专员']:
    exists = AdminRole.find().where(name=name).exists()
    if not exists:
        AdminRole(name=name).save()

fp = open('tests/admin.txt', 'r')
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

fp = open('tests/admin_auth.txt', 'r')
for line in fp:
    line = line.strip('\r\n')
    role, action = line.split()
    model = AdminAuth()
    model.role = role
    model.action = action
    model.save()
fp.close()
