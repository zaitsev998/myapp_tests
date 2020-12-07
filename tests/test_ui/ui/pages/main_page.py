from .base_page import BasePage
from ..locators.myapp_locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()
