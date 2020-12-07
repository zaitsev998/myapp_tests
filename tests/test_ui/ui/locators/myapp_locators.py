from selenium.webdriver.common.by import By


class BasePageLocators(object):
    USERNAME_FIELD = (By.ID, 'username')
    PASSWORD_FIELD = (By.ID, 'password')


class AuthPageLocators(BasePageLocators):
    LOGIN_BUTTON = (By.ID, 'submit')
    CREATE_AN_ACCOUNT_LINK = (By.XPATH, '//a[@href="/reg" and contains(text(), "Create an account")]')


class RegistrationPageLocators(BasePageLocators):
    EMAIL_FIELD = (By.ID, 'email')
    CONFIRM_PASS_FIELD = (By.ID, 'confirm')
    ACCEPT_TERM_CHECKBOX = (By.ID, 'term')
    REGISTER_BUTTON = (By.ID, 'submit')
    LOG_IN_LINK = (By.XPATH, '//a[@href="/login" and contains(text(), "Log in")]')


class MainPageLocators(BasePageLocators):
    LOGOUT_BUTTON = (By.XPATH, '//a[@href="/logout"]')
    WHAT_IS_AN_API = (By.XPATH, '//img[@src="/static/images/laptop.png"]')
    FUTURE_OF_INTERNET = (By.XPATH, '//img[@src="/static/images/loupe.png"]')
    SMTP = (By.XPATH, '//img[@src="/static/images/analytics.png"]')
    HOME_BUTTON = (By.XPATH, '//a[@href="/" and contains(text(), "HOME")]')
    PYTHON = (By.XPATH, '//a[contains(text(), "Python")]')
    LINUX = (By.XPATH, '//a[contains(text(), "Linux")]')
    NETWORK = (By.XPATH, '//a[contains(text(), "Network")]')
    PYTHON_HISTORY = (By.XPATH, '//a[contains(text(), "Python history")]')
    ABOUT_FLASK = (By.XPATH, '//a[contains(text(), "About Flask")]')
    DOWNLOAD_CENTOS = (By.XPATH, '//a[contains(text(), "Download Centos7")]')
    WIRESHARK_NEWS = (By.XPATH, '//li[contains(text(), "Wireshark")]//a[contains(text(), "News")]')
    WIRESHARK_DOWNLOAD = (By.XPATH, '//li[contains(text(), "Wireshark")]//a[contains(text(), "Download")]')
    TCPDUMP_EXAMPLES = (By.XPATH, '//li[contains(text(), "Tcpdump")]//a[contains(text(), "Examples")]')
    PYTHON_FACT = (By.XPATH, '//footer/div/p[2]')

    @staticmethod
    def LOGGED_AS(username):
        locator = (By.XPATH, f'//li[contains(text(), "Logged as {username}")]')
        return locator

    @staticmethod
    def VK_ID(vk_id):
        locator = (By.XPATH, f'//li[contains(text(), "VK ID: {vk_id}")]')
        return locator
