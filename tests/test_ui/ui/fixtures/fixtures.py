import pytest
from selenium import webdriver
from selenium.webdriver.support.abstract_event_listener import AbstractEventListener
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
import allure
from ..pages.base_page import BasePage
from ..pages.auth_page import AuthPage
from ..pages.main_page import MainPage
from ..pages.registration_page import RegistrationPage
from selenium.webdriver import ChromeOptions


class UnsupportedBrowserException(Exception):
    pass


@pytest.fixture
def base_page(driver):
    return BasePage(driver=driver)


@pytest.fixture
def auth_page(driver):
    return AuthPage(driver=driver)


@pytest.fixture
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture
def registration_page(driver):
    return RegistrationPage(driver=driver)


@pytest.fixture(scope='function')
def driver(config):
    selenoid = config['selenoid']
    url = config['url']
    browser = config['browser']
    if browser == 'chrome':
        options = ChromeOptions()
    else:
        raise UnsupportedBrowserException(f"Unsupported browser {browser}")
    driver = webdriver.Remote(command_executor=f"http://{selenoid}/wd/hub",
                              options=options,
                              desired_capabilities={'acceptInsecureCerts': True})
    driver.get(url=url)
    driver.maximize_window()
    yield driver
    driver.quit()

