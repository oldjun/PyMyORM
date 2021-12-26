from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)

    tables = Database.tables()
    for table in tables:
        filename = table.replace('t_', '')
        Database.model(table=table, filename=f'models/test/test/{filename}.py')
