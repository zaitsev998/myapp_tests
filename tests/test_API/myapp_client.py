import requests
from urllib.parse import urljoin


class MyAppClient:

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
