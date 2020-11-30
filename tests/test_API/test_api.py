import requests
import pytest
import allure
from faker import Faker
from random import randint
import json


class TestApi:
    fake = Faker(locale='en_US')

    @pytest.mark.skip
    def test_add_user(self, myapp_client):
        location = "/api/add_user"
        headers = {
            "Content-Type": "application/json"
        }
        password = self.fake.email()
        body = {
            "username": self.fake.first_name() + str(randint(1, 100)),
            "password": self.fake.password(),
            "email": password,
        }
        body = json.dumps(body)
        resp = myapp_client.request(method="POST", location=location, headers=headers, data=body)
        assert resp.status_code == 201
        assert resp.text == 'User was added!'
    #     TODO проверка бд

    @pytest.mark.skip
    def test_delete_user(self, myapp_client):
        # предварительно создать польз
        url = f"/api/del_user/Zaa019"
        resp = requests.get(url=url)
        print(resp.status_code)

    def test_block_user(self, myapp_client):
        # предварительно создать польз
        pass

    def test_unlock_user(self, myapp_client):
        # предварительно создать польз
        pass

    def test_app_status(self, myapp_client):
        location = "status"
        resp = myapp_client.request("GET", location=location)
        assert resp.status_code == 200
        assert eval(resp.text)['status'] == 'ok'


class TestApiNegative:

    pass

