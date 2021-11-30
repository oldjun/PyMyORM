#PyMyORM
---
Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example](#example)
* [Resources](#resource)
* [License](#license)

This package contains a pure-Python MySQL `Object Relational Mapping` client library.

##<a id=#requirements>Requirements</a>

* Python:
    *  [CPython](https://www.python.org/): 3.6 or newer
    *  [PyMySQL](https://github.com/PyMySQL/PyMySQL): 0.9.0 or newer
* MySQL server -- one of the following:
    * [MySQL](https://www.mysql.com/) >= 5.6
    * [MariaDB](https://mariadb.org/) >= 10.0

##<a id=#installation>Installation</a>
Package is uploaded on [PyPI](https://pypi.org/project/PyMyORM/).

You can install it with pip:
```shell
$python3 pip install PyMyORM
```

##<a href=#documentation>Documentation</a>
Documentation is coming soon.

##<a href=#example>Example</a>

The following examples make use of a simple table

```sql
create table `t_user` (
    `id` int unsigned not null auto_increment,
    `name` varchar(16) not null default '',
    `phone` varchar(16) not null default '',
    `money` decimal(10,2) not null default 0,
    `gender` tinyint unsigned not null default 0,
    `status` tinyint unsigned not null default 0,
    `time` timestamp not null default current_timestamp,
    primary key(`id`),
    unique key `idx_name` (`name`),
    key `idx_phone` (`phone`),
    key `idx_status` (`status`),
    key `idx_time` (`time`)
) engine=InnoDB auto_increment=1 default charset=utf8mb4;
```

Model definition models/user.py
```python
from pymyorm.model import Model

class User(Model):
    tablename = 't_user'
```

Connect to database
```python
from pymyorm.database import Database
Database().connect(host='127.0.0.1',
                   port=3306,
                   user='root',
                   password='password',
                   database='test',
                   charset='utf8'
                   )
```
###select

```python
# case 1
from models.user import User
one = User.find().where(name='ping').one()
print(one.id, one.name)
```

```python
# case 2
from models.user import User
one = User.find().select('name').where(name='ping').where(phone='18976641111').one()
print(one)
```

```python
# case 3
from models.user import User
one = User.find().where(name='ping', phone='18976641111').one()
print(one)
```

```python
# case 4
from models.user import User
one = User.find().where('money', '!=', 200).order('id desc').one()
print(one)
```

```python
# case 6
from models.user import User
all = User.find().order('id desc').offset(0).limit(5).all()
for one in all:
    print(one)
```

###update

```python
# case 1
from models.user import User
one = User.find().where(name='lily').one()
one.money = 500
one.phone = '18976642222'
one.save()
```

```python
# case 2
from models.user import User
User.find().where(name='lily').update(money=500, phone='18976642222')
```

###insert

```python
# case 1
from models.user import User
user = User(name='rose', phone='18976643333', money=100)
user.save()
```

```python
# case 2
from models.user import User
user = User()
user.name = 'vera'
user.phone = '18976644444'
user.money = 100
user.save()
```

###delete

```python
# case 1
from models.user import User
one = User.find().where(name='lily').one()
one.delete()
```

```python
# case 2
from models.user import User
User.find().where(money=100).delete()
```

```python
# case 3
from models.user import User
all = User.find().select('name', 'phone').where('money', '>', 100).all()
for one in all:
    one.delete()
```

```python
# case 4
from models.user import User
User.find().delete() # delete all users
```

###exists

```python
from models.user import User
exists = User.find().where(name='ping').exists()
```

###count

```python
from models.user import User
count = User.find().where(status='0').count()
```

###min

```python
from models.user import User
money = User.find().where(status=0).min('money')
```

###max

```python
from models.user import User
money = User.find().where(status=0).max('money')
print(money)
```

###average

```python
from models.user import User
money = User.find().where(status=0).average('money')
```

###scalar

```python
from models.user import User
money = User.find().where(id=1).scalar('money')
```

###column

```python
from models.user import User
names = User.find().column('name')
```

###truncate

```python
from models.user import User
User.find().truncate()
```

###join

```python
# case 1: inner join
from models.admin import Admin
from models.admin_role import AdminRole
all = Admin.find().select('a.*').alias('a') \
    .join(table=AdminRole.tablename, alias='r', on='a.role = r.id') \
    .where('r.name', '=', 'role1') \
    .where('a.lock', '=', 0) \
    .all()
for one in all:
    print(one)
```

```python
# case 2: left join
from models.admin import Admin
from models.admin_role import AdminRole
all = Admin.find().alias('a') \
    .join(table=AdminRole.tablename, alias='r', on='a.role=r.id', type='left') \
    .where('a.lock', '=', 0) \
    .all()
for one in all:
    print(one)
```

```python
# case 3
from models.admin import Admin
from models.admin_role import AdminRole
all = Admin.find().select('a.*').alias('a') \
    .join(table=AdminRole.tablename, alias='r', on='a.role=r.id') \
    .where('a.lock', '=', 0) \
    .all()
for one in all:
    print(one)
```

```python
# case 4: join more than one table
from models.admin import Admin
from models.admin_role import AdminRole
from models.admin_auth import AdminAuth
all = Admin.find().select('username', 'a.role').alias('a') \
    .join(table=AdminRole.tablename, alias='r', on='a.role=r.id') \
    .join(table=AdminAuth.tablename, alias='t', on='t.role=r.id') \
    .where('t.action', '=', 300) \
    .all()
for one in all:
    print(one)
```

### transaction

```python
# case 1
from pymyorm.transaction import Transaction as t
from models.user import User
try:
    t.begin()
    model = User(name='ping', phone='18976641111', money=100)
    model.save()
    t.commit()
except Exception as e:
    t.rollback()
    raise e
```

```python
# case 2 : nested transaction
from pymyorm.transaction import Transaction as t
try:
    t.begin()
    # ... your code
    try:
        t.begin()
        # ... your code
        t.commit()
    except Exception as e:
        t.rollback()
        raise e
    t.commit()
except Exception as e:
    t.rollback()
    raise e
```

##<a href=#resource>Resource</a>

* MySQL Reference Manuals: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* PyMySQL: [https://pymysql.readthedocs.io/](https://pymysql.readthedocs.io/)

##<a href=#license>License</a>

PyMyORM is released under the MIT License. See LICENSE for more information.
