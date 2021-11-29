from demos.config import db
from pymyorm.database import Database

fp = open('sql/t_user.sql', 'r', encoding='utf-8')
sql = fp.read()
fp.close()

d = Database()
d.connect(**db)
d.execute(sql)
