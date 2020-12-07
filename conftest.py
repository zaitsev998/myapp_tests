import pytest
import tests.test_settings as ts
from tests.test_API.myapp_client import MyAppClient
from database.code.mysql_orm_client import MysqlOrmConnection
from database.code.mysql_orm_builder import MysqlOrmBuilder
from tests.test_ui.ui.fixtures.fixtures import *
import allure


def pytest_addoption(parser):
    parser.addoption('--selenoid', default=f'{ts.SELENOID_HOST}:{ts.SELENOID_PORT}')
    parser.addoption('--url', default=f'http://{ts.APP_HOST}:{ts.APP_PORT}/')
    parser.addoption('--browser', default='chrome')


@pytest.fixture(scope='session')
def config(request):
    selenoid = request.config.getoption('--selenoid')
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    return {'browser': browser, 'url': url, 'selenoid': selenoid}


@pytest.fixture(scope='session')
def myapp_client():
    yield MyAppClient(ts.APP_HOST, ts.APP_PORT, ts.APP_USER, ts.APP_PASS)


@pytest.fixture(scope='session')
def mysql():
    conn = MysqlOrmConnection(ts.DB_USER, ts.DB_PASS, ts.DB_NAME, ts.DB_HOST, ts.DB_PORT)
    yield MysqlOrmBuilder(conn)


def pytest_exception_interact(node, call, report):
    try:
        driver = node.instance.driver
    except:
        pass
    else:
        allure.attach(driver.get_screenshot_as_png())
