from models import Base, TestUser
from mysql_orm_client import MysqlOrmConnection


class MysqlOrmBuilder(object):
    def __init__(self, connection: MysqlOrmConnection):
        self.connection = connection
        self.engine = self.connection.connection.engine
        self.create_log()

    def create_log(self):
        if not self.engine.dialect.has_table(self.engine, 'test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def add_user(self, username, password, email, access=1):

        test_user = TestUser(
            username=username,
            password=password,
            email=email,
            access=access
        )

        self.connection.session.add(test_user)
        self.connection.session.commit()
        return test_user
