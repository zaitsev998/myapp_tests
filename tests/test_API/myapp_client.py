import json
from random import randint
import requests
from urllib.parse import urljoin
from faker import Faker


class MyAppClient:
    fake = Faker(locale='en_US')

    def __init__(self, host, port, username, password):
        self.base_url = f"http://{host}:{port}/"
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.login()

    def login(self):
        url = urljoin(self.base_url, 'login')
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "username": self.username,
            "password": self.password,
            "submit": "Login"
        }
        self.session.post(url=url, headers=headers, data=body)

    def request(self, method, location, headers=None, data=None, params=None):
        url = urljoin(self.base_url, location)
        response = self.session.request(method, url, headers=headers, params=params, data=data)
        return response

    def create_user(self, mysql, username=None, password=None, email=None, access=1):
        if username is None:
            username = self.fake.first_name() + str(randint(10000, 100000))
        if password is None:
            password = self.fake.password()
        if email is None:
            email = self.fake.email()
        mysql.add_user(username=username, password=password, email=email, access=access)
        return {
            'username': username,
            'password': password,
            'email': email
        }

    def create_user_by_api(self, username, password, email):
        location = "/api/add_user"
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "username": username,
            "password": password,
            "email": email,
        }
        data = json.dumps(body)
        return self.request(method="POST", location=location, headers=headers, data=data)

