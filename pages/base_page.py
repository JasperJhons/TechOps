from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


class BasePage(object):
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_title(self):
        return self.driver.title

    def driver_wait(self, timeout=10):
        return WebDriverWait(self.driver, timeout)
