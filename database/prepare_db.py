import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import Base, TestUser


class MysqlOrmConnection(object):

    def __init__(self, user, password, db_name, host, port):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.port = port
        self.host = host
        self.connection = self.connect()
        session = sessionmaker(bind=self.connection)
        self.session = session()

    def get_connection(self, db_created=False):
        engine = sqlalchemy.create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            db=self.db_name if db_created else ''
        ))
        return engine.connect()

    def connect(self):
        connection = self.get_connection(db_created=False)

        connection.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
        connection.execute(f'CREATE DATABASE {self.db_name}')

        connection.close()

        return self.get_connection(db_created=True)


if __name__ == '__main__':
    connection = MysqlOrmConnection('root', 'pass', 'MYSQL_DB', host='0.0.0.0', port=3306)
    engine = connection.connection.engine
    if not engine.dialect.has_table(engine, 'test_users'):
        Base.metadata.tables['test_users'].create(engine)
