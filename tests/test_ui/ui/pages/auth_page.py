from .base_page import BasePage
from ..locators.myapp_locators import AuthPageLocators


class AuthPage(BasePage):
    locators = AuthPageLocators()

    def auth_user(self, username, password):
        self.driver.get(f"http://myapp:8888/login")
        username_field = self.find(self.locators.USERNAME_FIELD)
        self.fill_field(username_field, username)
        password_field = self.find(self.locators.PASSWORD_FIELD)
        self.fill_field(password_field, password)
        self.click(self.locators.LOGIN_BUTTON)
