import sqlalchemy
from sqlalchemy.orm import sessionmaker


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

        connection.execute(f'CREATE DATABASE IF NOT EXISTS {self.db_name}')
        connection.close()

        return self.get_connection(db_created=True)