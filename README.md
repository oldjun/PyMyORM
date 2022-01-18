PyMyORM
---
Table of Contents

* [Requirements](#requirements)
* [Installation](#installation)
* [Documentation](#documentation)
* [Example](#example)
* [Resources](#resource)
* [License](#license)

This package contains a pure-Python MySQL `Object Relational Mapping` client library.

## <a href=#requirements>Requirements</a>

* Python:
    *  [CPython](https://www.python.org/): 3.6 or newer
    *  [PyMySQL](https://github.com/PyMySQL/PyMySQL): 0.9.0 or newer
* MySQL server -- one of the following:
    * [MySQL](https://www.mysql.com/) >= 5.6
    * [MariaDB](https://mariadb.org/) >= 10.0

## <a href=#installation>Installation</a>

Package is uploaded on [PyPI](https://pypi.org/project/PyMyORM/).

You can install it with pip:

```shell
$python3 pip install PyMyORM
```

## <a href=#documentation>Documentation</a>
Documentation is coming soon.

## <a href=#example>Example</a>

### table

The following examples use a simple table

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

### model
the simplest definition of a model

```python
from pymyorm.model import Model

class User(Model):
    tablename = 't_user'
```

by default model's primary key is `id`, if your table's primary key isn't `id`, you can adjust the model class's attributes like this:

```python
from pymyorm.model import Model

class User(Model):
    tablename = 't_user'
    primary_key = 'this is table primary key'
```

if your table contains at least one datetime column or decimal column, you probably like to auto format the column's value from datetime to string,
or from decimal to float, you can do it like this

```python
from pymyorm.model import Model

class User(Model):
    tablename = 't_user'
    datetime_fields = ['create_time', 'update_time']
    decimal_fields = ['money']
```

### connect

connect to database at a single thread mode

```python
from pymyorm.database import Database
config = dict(host='127.0.0.1', port=3306, user='root', password='password', database='test')
Database.connect(**config)
```

if your program is running at multi thread mode, you should use connection pool instead.
see the connection pool section.

### raw sql

sometimes we need to execute sql statement, like creating tables, do it like below.

```python
from pymyorm.database import Database
fp = open('sql/t_user.sql', 'r', encoding='utf-8')
sql = fp.read()
fp.close()

Database.connect(**config)
Database.execute(sql)
```

```python
from pymyorm.database import Database
from config import db

Database.connect(**db)
sql = "select * from t_user"
all = Database.query(sql)
for one in all:
    print(one)
```

### tables

```python
from pymyorm.database import Database
from config import db

Database.connect(**db)
tables = Database.tables()
for table in tables:
    print(table)
```

### schema

```python
from pymyorm.database import Database
from config import db

Database.connect(**db)
schemas = Database.schema('t_user')
for schema in schemas:
    print(schema)
```

### reflection

```python
from pymyorm.database import Database
from config import db

Database.connect(**db)
Database.model(table='t_user', model='models/user.py')
```

### select

find one user which name is 'ping'

```python
from models.user import User
one = User.find().where(name='ping').one()
print(one.id, one.name)
```

find one user which name is 'ping' and phone is '18976641111'

```python
from models.user import User
one = User.find().where(name='ping').where(phone='18976641111').one()
print(one)
```

find one user which name is 'ping' and phone is '18976641111', in another way

```python
from models.user import User
one = User.find().where(name='ping', phone='18976641111').one()
print(one)
```

find one user which money is not equals to 200

```python
from models.user import User
one = User.find().where('money', '!=', 200).one()
print(one)
```

```python
from models.user import User
all = User.find().order('id desc').offset(0).limit(5).all()
for one in all:
    print(one)
```

### batch select

the all() function will return all data which matched the where conditions, if the table is too big, it will cost too much memory and slow down the program.

in this situation we can use batch() instead of all(). the code slice below shows each time read 100 users, until all to the end.

```python
from models.user import User
batch = User.find().batch(size=100)
for all in batch:
    for one in all:
        print(one)
```

### where

where condition support ternary operator: =, !=, <, <=, >=, >, in, not in, like, not like, is, is not, between

### update

find the user which name is 'lily', and change her money to 500, her phone to '18976642222'

```python
from models.user import User
one = User.find().where(name='lily').one()
one.money = 500
one.phone = '18976642222'
one.save()
```

change the user which name is 'lily', update her money and phone directly

```python
# case 2
from models.user import User
User.find().where(name='lily').update(money=500, phone='18976642222')
```

### insert

insert one user into table

```python
# case 1
from models.user import User
user = User(name='rose', phone='18976643333', money=100)
user.save()
```

insert one user into table, in another way

```python
# case 2
from models.user import User
user = User()
user.name = 'vera'
user.phone = '18976644444'
user.money = 100
user.save()
```

### batch insert

the save() function only insert/update one data at a time.
we can use insert() function to insert more than one data at a time to improve the performance.

```python
from models.user import User
fields = ('name', 'phone', 'money')
values = [
    ('jack', '18976643333', 120),
    ('sean', '18976654444', 160),
    ('vera', '18976645555', 180),
]
User.insert(fields, values)
```

### delete

find the user which name is 'lily', and delete it

```python
from models.user import User
one = User.find().where(name='lily').one()
one.delete()
```

delete the user which name is 'lily' directly

```python
from models.user import User
User.find().where(money=100).delete()
```

find users which money more than 100, and delete it one by one

```python
from models.user import User
all = User.find().where('money', '>', 100).all()
for one in all:
    one.delete()
```

delete the users which money more than 100 directly

```python
from models.user import User
User.find().where('money', '>', 100).delete()
```

delete all users, don't do this if you don't know what you are doing.

```python
from models.user import User
User.find().delete()
```

### exists

find the user which name is 'ping' is exists or not, return True or False rather than the user data

```python
from models.user import User
exists = User.find().where(name='ping').exists()
```

### count

count the number of users which status is equal to 0

```python
from models.user import User
count = User.find().where(status=0).count()
```

### sum

sum of user's money

```python
from models.user import User
money = User.find().sum('money')
```

### min

find the minimal money of users, return the minimal money rather than the user data

```python
from models.user import User
money = User.find().where(status=0).min('money')
```

### max

find the maximal money of users, return the maximal money rather than the user data

```python
from models.user import User
money = User.find().where(status=0).max('money')
print(money)
```

### average

calculate the average money of the users, return the average money rather than the user data

```python
from models.user import User
money = User.find().where(status=0).average('money')
```

### scalar

find the user's money which name is jack

```python
from models.user import User
money = User.find().where(name='jack').scalar('money')
```

### column

list all user's name

```python
from models.user import User
names = User.find().column('name')
```

### group by

group the users by gender, and calculate the average money of each group, and return the users which group average money are more than 220

```python
from models.user import User
all = User.find() \
    .select('gender', 'count(*) as count', 'avg(money) as avg', 'sum(money) as total') \
    .group('gender') \
    .having('avg', '>', 220) \
    .all()
for one in all:
    print(one)
```

### group count

group the users by gender, and get the total number of groups

```python
from models.user import User
total = User.find().group('gender').count()
print(total)
```

### truncate

truncate the user table, don't do this if you don't know what you are doing.

```python
from models.user import User
User.truncate()
```

### join

find admin which role is 'roles' and which lock is 0

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

### ping

As mysql server's default wait timeout is 28800 seconds, it means that after 8 hours if connection is stay sleep, the server will disconnect it.
to prevent this problem, each connection should have ability to auto reconnect, by default PyMyORM's each connection will ping mysql server after 3600 seconds idle or sleep.
you can change the ping interval by the flow code slice:

```python
pool = ConnectionPool()
pool.size(size=8)
pool.ping(seconds=7200)
pool.create(**db)
```

as you see, it will change the default ping interval time from 3600 to 7200 seconds. how much long about the ping interval depends on your mysql server's wait timeout configuration. you should set the ping interval less than your server's wait timeout.
login your mysql server , and run the following sql to see the wait timeout

```sql
show variables like '%wait_timeout%';
```

### auto reconnect

mysql server maybe reboot because some reason, but don't worry about it.
PyMyORM has take care about this situation, each connetion will auto re-connect immediately if the connection has gone.

### connection pool

By default PyMyORM works at single thread, however when we develop a web application based on flask, we would like to make PyMyORM support multi-threading.

So PyMyORM provide a connection pool component, and it's threadsafety.

In this kind of scenario, we should use ConnectionPool to replace Database to init mysql connection.

```python
import functools
from flask import Flask
from pymyorm.local import local
from pymyorm.connection_pool import ConnectionPool
from models.user import User

app = Flask(__name__)

config = dict(user=user, port=port, user=user, password=password, database=database)
pool = ConnectionPool()
pool.size(size=10)
pool.debug(debug=True)
pool.create(**config)


# assign one connection to the request
def assign_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pool = ConnectionPool()
        local.conn = pool.get()
        
        resp = func(*args, **kwargs)
        # don't forget to put connection into pool
        pool.put(local.conn)
        return resp
    return wrapper

@app.route('/')
@assign_connection
def index():
    one = User.find().where(name='ping').one()
    print(one)
    return 'index'

@app.route('/hello')
@assign_connection
def hello():
    one = User.find().where(name='ping').one()
    print(one)
    return 'hello'
```

As the code slice mentioned above, PyMyORM assign one mysql connection for each
http request, so the mysql transaction will work properly.

## <a href=#resource>Resource</a>

* MySQL Reference Manuals: [https://dev.mysql.com/doc/](https://dev.mysql.com/doc/)
* PyMySQL: [https://pymysql.readthedocs.io/](https://pymysql.readthedocs.io/)

## <a href=#license>License</a>

PyMyORM is released under the MIT License. See LICENSE for more information.
