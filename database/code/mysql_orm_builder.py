from database.code.models import Base, TestUser
from database.code.mysql_orm_client import MysqlOrmConnection
import datetime


class MysqlOrmBuilder(object):
    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = self.connection.connection.engine
        self.create_table()

    def create_table(self):
        if not self.engine.dialect.has_table(self.engine, 'test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def add_user(self, username, password, email, access=1):

        test_user = TestUser(
            username=username,
            password=password,
            email=email,
            access=access,
            active=0,
            start_active_time=datetime.datetime.now()
        )

        self.connection.session.add(test_user)
        self.connection.session.commit()
        return test_user
