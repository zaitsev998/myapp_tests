from selenium.webdriver import ActionChains

from ..locators.myapp_locators import BasePageLocators
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException

RETRY_COUNT = 3


class BasePage(object):
    locators = BasePageLocators()

    def __init__(self, driver):
        self.driver = driver

    def find(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    @staticmethod
    def fill_field(field, value):
        field.clear()
        field.send_keys(value)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        for i in range(RETRY_COUNT):
            try:
                self.find(locator)
                element = self.wait(timeout).until(EC.element_to_be_clickable(locator))
                element.click()
                return

            except StaleElementReferenceException:
                if i < RETRY_COUNT - 1:
                    pass
        raise

    def go_to_element(self, locator):
        element = self.find(locator)
        ac = ActionChains(self.driver)
        ac.move_to_element(element).perform()