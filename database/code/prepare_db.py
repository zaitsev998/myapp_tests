from sqlalchemy.exc import OperationalError
import settings
import time
from mysql_orm_builder import MysqlOrmBuilder
from mysql_orm_client import MysqlOrmConnection


if __name__ == '__main__':
    while True:
        try:
            connection = MysqlOrmConnection('root', 'pass', settings.DB_NAME, settings.DB_HOST, settings.DB_PORT)
        except OperationalError:
            time.sleep(3)
            continue
        break
    builder = MysqlOrmBuilder(connection)
    builder.connection.connection.execute(f"CREATE USER '{settings.DB_USER}' IDENTIFIED BY '{settings.DB_PASS}';")
    builder.connection.connection.execute(f"GRANT ALL PRIVILEGES ON * . * to '{settings.DB_USER}';")
    builder.connection.connection.execute("FLUSH PRIVILEGES;")
    builder.add_user(username=settings.APP_USER, password=settings.APP_PASS, email='some_email@mail.ru', access=1)
