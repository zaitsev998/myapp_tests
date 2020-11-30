import pytest
import tests.test_settings as ts
from tests.test_API.myapp_client import MyAppClient
from database.code.mysql_orm_client import MysqlOrmConnection
from database.code.mysql_orm_builder import MysqlOrmBuilder


@pytest.fixture(scope='session')
def myapp_client():
    yield MyAppClient(ts.APP_HOST, ts.APP_PORT, ts.APP_USER, ts.APP_PASS)


@pytest.fixture(scope='session')
def mysql():
    conn = MysqlOrmConnection(ts.DB_USER, ts.DB_PASS, ts.DB_NAME, ts.DB_HOST, ts.DB_PORT)
    yield MysqlOrmBuilder(conn)