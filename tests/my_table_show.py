from pymyorm.database import Database
from config import db


if __name__ == '__main__':
    Database.connect(**db)
    tables = Database.tables()
    for table in tables:
        print(table)
        schemas = Database.schema(table)
        for schema in schemas:
            print(schema)
