from pymyorm.database import Database
from config import db
from models.admin import Admin
from models.admin_role import AdminRole


if __name__ == '__main__':

    Database.connect(**db)

    exists = Admin.find().select('a.*').alias('a') \
        .join(table=AdminRole.tablename, alias='r', on='a.role = r.id') \
        .where('r.name', '=', 'role1') \
        .where('a.lock', '=', 0) \
        .exists()
    if exists:
        print('exists')
    else:
        print('not exists')
