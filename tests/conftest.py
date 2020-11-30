import pytest
import test_settings as ts
from test_API.myapp_client import MyAppClient


@pytest.fixture(scope='session')
def myapp_client():
    yield MyAppClient(ts.APP_HOST, ts.APP_PORT, ts.APP_USER, ts.APP_PASS)

