import json

from selenium.webdriver import ActionChains
from seleniumwrapper import SeleniumWrapper
import allure
import requests
from database.code.models import TestUser
from ui.pages.auth_page import AuthPage
from ui.pages.main_page import MainPage
from ui.pages.registration_page import RegistrationPage
from ui.pages.base_page import BasePage
from _pytest.fixtures import FixtureRequest
import pytest
from faker import Faker
from random import randint

fake = Faker(locale="en_US")


class BaseCase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, mysql, myapp_client, request: FixtureRequest):
        self.driver = driver
        self.config = config
        self.mysql = mysql
        self.myapp_client = myapp_client
        self.base_page: BasePage = request.getfixturevalue('base_page')
        self.auth_page: AuthPage = request.getfixturevalue('auth_page')
        self.main_page: MainPage = request.getfixturevalue('main_page')
        self.registration_page: RegistrationPage = request.getfixturevalue('registration_page')

    def switch_tab_if_possible(self):
        tabs = self.driver.window_handles
        if len(tabs) > 1:
            self.driver.switch_to.window(tabs[1])


class TestAuthPage(BaseCase):

    def test_auth(self):
        user = self.myapp_client.create_user(self.mysql)
        self.auth_page.auth_user(user['username'], user['password'])
        db_resp = self.mysql.connection.session.query(TestUser).filter_by(username=user['username'])
        assert f'Logged as {user["username"]}' in self.driver.page_source
        assert (db_resp[0].access, db_resp[0].active) == (1, 1)


class TestAuthPageNegative(BaseCase):

    def test_wrong_username(self):
        username = fake.last_name() + str(randint(101, 200))
        password = fake.password()
        self.auth_page.auth_user(username, password)
        assert 'Invalid username or password' in self.driver.page_source

    def test_wrong_password(self):
        user = self.myapp_client.create_user(self.mysql)
        password = fake.password()
        self.auth_page.auth_user(user['username'], password)
        assert 'Invalid username or password' in self.driver.page_source

    def test_auth_without_access(self):
        user = self.myapp_client.create_user(self.mysql, access=0)
        self.auth_page.auth_user(user["username"], user["password"])
        assert 'Ваша учетная запись заблокирована' in self.driver.page_source


class TestRegistrationPage(BaseCase):

    def test_register(self):
        username = fake.first_name() + str(randint(1000, 1000000))
        password = fake.password()
        email = fake.email()
        self.registration_page.register_user(username, email, password)
        db_resp = self.mysql.connection.session.query(TestUser).filter_by(username=username)
        assert f'Logged as {username}' in self.driver.page_source
        assert (db_resp[0].access, db_resp[0].active) == (1, 1)

    def test_log_in_link(self):
        self.driver.get("http://myapp:8888/reg")
        self.registration_page.click(self.registration_page.locators.LOG_IN_LINK)
        assert 'Welcome to the TEST SERVER' in self.driver.page_source


class TestRegistrationPageNegative(BaseCase):

    def test_wrong_username(self):
        username = str(randint(1, 100))
        password = fake.password()
        email = fake.email()
        self.registration_page.register_user(username, email, password)
        assert "Incorrect username length" in self.driver.page_source

    def test_short_email(self):
        username = fake.first_name() + str(randint(1, 100))
        password = fake.password()
        email = str(randint(1, 100))
        self.registration_page.register_user(username, email, password)
        assert 'Incorrect email length' in self.driver.page_source

    def test_wrong_email(self):
        username = fake.first_name() + str(randint(1, 100))
        password = fake.password()
        email = fake.first_name() + '@' + 'mail'
        self.registration_page.register_user(username, email, password)
        assert 'Invalid email address' in self.driver.page_source

    def test_passwords_not_match(self):
        username = fake.first_name() + str(randint(1, 100))
        password = fake.password()
        email = fake.email()
        self.registration_page.register_user(username, email, password, fake.password())
        assert 'Passwords must match' in self.driver.page_source

    def test_existing_username(self):
        user = self.myapp_client.create_user(self.mysql)
        self.registration_page.register_user(user["username"], fake.email(), fake.password())
        assert "User already exist" in self.driver.page_source

    def test_existing_email(self):
        user = self.myapp_client.create_user(self.mysql)
        self.registration_page.register_user(fake.first_name() + str(randint(1, 100)), user["email"], fake.password())
        assert "Email already exist" in self.driver.page_source


class TestMainPage(BaseCase):

    @pytest.fixture(scope='function')
    def create_and_authorize(self):
        user = self.myapp_client.create_user(self.mysql)
        self.auth_page.auth_user(username=user["username"], password=user["password"])
        self.user = user

    def test_what_is_an_api_link(self, create_and_authorize):
        self.main_page.click(self.main_page.locators.WHAT_IS_AN_API)
        self.switch_tab_if_possible()
        assert "API" in self.driver.page_source

    def test_future_of_the_internet_link(self, create_and_authorize):
        self.main_page.click(self.main_page.locators.FUTURE_OF_INTERNET)
        self.switch_tab_if_possible()
        assert "future of the internet" in self.driver.page_source

    def test_SMTP_link(self, create_and_authorize):
        self.main_page.click(self.main_page.locators.SMTP)
        self.switch_tab_if_possible()
        assert "SMTP" in self.driver.page_source

    def test_python_link(self, create_and_authorize):
        self.main_page.click(self.main_page.locators.PYTHON)
        self.switch_tab_if_possible()
        assert "python" in self.driver.page_source

    def test_python_history_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.PYTHON)
        self.main_page.click(self.main_page.locators.PYTHON_HISTORY)
        self.switch_tab_if_possible()
        assert "python" in self.driver.page_source and "history" in self.driver.page_source

    def test_about_flask_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.PYTHON)
        self.main_page.click(self.main_page.locators.ABOUT_FLASK)
        self.switch_tab_if_possible()
        assert "Flask" in self.driver.page_source

    def test_download_centos_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.LINUX)
        self.main_page.click(self.main_page.locators.DOWNLOAD_CENTOS)
        self.switch_tab_if_possible()
        assert "CentOS" in self.driver.page_source or "centos" in self.driver.page_source or \
               "Centos" in self.driver.page_source

    def test_wireshark_news_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.NETWORK)
        self.main_page.click(self.main_page.locators.WIRESHARK_NEWS)
        self.switch_tab_if_possible()
        assert "Wireshark" in self.driver.page_source and "News" in self.driver.page_source

    def test_wireshark_download_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.NETWORK)
        self.main_page.click(self.main_page.locators.WIRESHARK_DOWNLOAD)
        self.switch_tab_if_possible()
        assert "Wireshark" in self.driver.page_source and "Download" in self.driver.page_source

    def test_tcpdump_examples_link(self, create_and_authorize):
        self.main_page.go_to_element(self.main_page.locators.NETWORK)
        self.main_page.click(self.main_page.locators.TCPDUMP_EXAMPLES)
        self.switch_tab_if_possible()
        assert "Tcpdump" in self.driver.page_source and "Examples" in self.driver.page_source

    def test_logout(self, create_and_authorize):
        self.main_page.click(self.main_page.locators.LOGOUT_BUTTON)
        db_resp = self.mysql.connection.session.query(TestUser).filter_by(username=self.user["username"])
        assert db_resp[0].active == 0 and 'Welcome to the TEST SERVER' in self.driver.page_source

    def test_vk_api(self):
        user = self.myapp_client.create_user(self.mysql)
        vk_id = randint(10000, 1000000)
        data = {
            "username": user["username"],
            "vk_id": vk_id
        }
        data = json.dumps(data)
        headers = {'Content-type': 'application/json',
                   'Content-Length': str(len(data))}
        requests.post("http://vk_api:5555/vk_id", data=data, headers=headers)
        self.auth_page.auth_user(username=user["username"], password=user["password"])
        assert self.main_page.find(self.main_page.locators.VK_ID(vk_id))

    def test_python_fact(self, create_and_authorize):
        assert self.main_page.find(self.main_page.locators.PYTHON_FACT)

    def test_display_username(self, create_and_authorize):
        assert self.main_page.find(self.main_page.locators.LOGGED_AS(self.user["username"]))

