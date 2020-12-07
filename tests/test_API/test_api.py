from faker import Faker
from random import randint
import json
from database.code.models import TestUser


class TestApi:
    fake = Faker(locale='en_US')

    def test_add_user(self, myapp_client, mysql):
        """
        Проверяет добавление пользователя через api.
        Генерируются фейковые(валидные) имя пользователя, пароль, e-mail.
        Данные отпраляются POST запросом на /api/add_user
        Ожидаем код ответа 201 и тело ответа User was added!
        Пытаемся получить данные о пользователе из БД (по имени пользователя)
        Ожидаем, что найден единственный пользователь и его данные совпадают с отправленными.

        :param myapp_client: коннектор к приложению
        :param mysql: коннектор к БД
        """
        location = "/api/add_user"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "username": self.fake.first_name() + str(randint(1, 100)),
            "password": self.fake.password(),
            "email": self.fake.email(),
        }
        data = json.dumps(body)
        resp = myapp_client.request(method="POST", location=location, headers=headers, data=data)
        db_resp = mysql.connection.session.query(TestUser).filter_by(username=body['username'])
        assert (resp.status_code, resp.text, len(list(db_resp)), db_resp[0].username, db_resp[0].password,
                db_resp[0].email) == (201, 'User was added!', 1, body['username'], body['password'], body['email'])

    def test_delete_user(self, myapp_client, mysql):
        user = myapp_client.create_user(mysql)
        location = f"/api/del_user/{user['username']}"
        resp = myapp_client.request(method="GET", location=location)
        db_resp = mysql.connection.session.query(TestUser).filter_by(username=user['username'])
        assert (resp.status_code, len(list(db_resp))) == (204, 0)

    def test_block_user(self, myapp_client, mysql):
        user = myapp_client.create_user(mysql)
        location = f"/api/block_user/{user['username']}"
        resp = myapp_client.request(method="GET", location=location)
        db_resp = mysql.connection.session.query(TestUser).filter_by(username=user['username'])
        assert (resp.status_code, resp.text, db_resp[0].access) == (200, 'User was blocked!', 0)

    def test_unlock_user(self, myapp_client, mysql):
        user = myapp_client.create_user(mysql, access=0)
        location = f"/api/accept_user/{user['username']}"
        resp = myapp_client.request(method="GET", location=location)
        db_resp = mysql.connection.session.query(TestUser).filter_by(username=user['username'])
        assert (resp.status_code, resp.text, db_resp[0].access) == (200, 'User access granted!', 1)

    def test_app_status(self, myapp_client):
        location = "status"
        resp = myapp_client.request("GET", location=location)
        assert (resp.status_code, eval(resp.text)['status']) == (200, 'ok')


class TestApiNegative:
    fake = Faker(locale='en_US')

    def test_add_user_wrong_email(self, myapp_client):
        resp = myapp_client.create_user_by_api(self.fake.first_name() + str(randint(1, 100)),
                                               self.fake.password(), self.fake.last_name())
        assert resp.status_code == 400

    def test_add_user_empty_username(self, myapp_client):
        resp = myapp_client.create_user_by_api('', self.fake.password(), self.fake.last_name())
        assert resp.status_code == 400

    def test_add_user_empty_password(self, myapp_client):
        resp = myapp_client.create_user_by_api(self.fake.first_name() + str(randint(1, 100)),
                                               '', self.fake.last_name())
        assert resp.status_code == 400

    def test_add_user_existing_username(self, myapp_client):
        username = self.fake.first_name() + str(randint(1, 100))
        myapp_client.create_user_by_api(username, self.fake.password(), self.fake.email())
        resp = myapp_client.create_user_by_api(username, self.fake.password(), self.fake.email())
        assert (resp.status_code, resp.text) == (304, '')

    def test_add_user_existing_email(self, myapp_client):
        email = self.fake.email()
        myapp_client.create_user_by_api(self.fake.first_name() + str(randint(1, 100)), self.fake.password(), email)
        resp = myapp_client.create_user_by_api(self.fake.first_name() + str(randint(1, 100)),
                                               self.fake.password(), email)
        assert (resp.status_code, resp.text == 304, '')

    def test_delete_user_negative(self, myapp_client):
        location = f"/api/del_user/{randint(1, 1000)}"
        resp = myapp_client.request(method="GET", location=location)
        assert (resp.status_code, resp.text) == (404, 'User does not exist!')

    def test_block_user_negative(self, myapp_client):
        location = f"/api/block_user/{randint(1, 1000)}"
        resp = myapp_client.request(method="GET", location=location)
        assert (resp.status_code, resp.text) == (404, 'User does not exist!')

    def test_unlock_user_negative(self, myapp_client):
        location = f"/api/accept_user/{randint(1, 1000)}"
        resp = myapp_client.request(method="GET", location=location)
        assert (resp.status_code, resp.text) == (404, 'User does not exist!')
