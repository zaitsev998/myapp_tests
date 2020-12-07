from .base_page import BasePage
from ..locators.myapp_locators import RegistrationPageLocators
# from .... import test_settings as ts


class RegistrationPage(BasePage):
    locators = RegistrationPageLocators()

    def register_user(self, username, email, password, repeat_password=None):
        self.driver.get(f"http://myapp:8888/reg")
        username_field = self.find(self.locators.USERNAME_FIELD)
        self.fill_field(username_field, username)
        email_field = self.find(self.locators.EMAIL_FIELD)
        self.fill_field(email_field, email)
        password_field = self.find(self.locators.PASSWORD_FIELD)
        self.fill_field(password_field, password)
        repeat_password_field = self.find(self.locators.CONFIRM_PASS_FIELD)
        if repeat_password is None:
            self.fill_field(repeat_password_field, password)
        else:
            self.fill_field(repeat_password_field, repeat_password)
        self.click(self.locators.ACCEPT_TERM_CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)

