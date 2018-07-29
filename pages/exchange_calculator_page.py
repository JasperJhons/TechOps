import allure
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from helpers.api_helper import ApiHelper
from helpers.currency_converter import CurrencyConverter
from pages.base_page import BasePage


class ExchangeCalculatorPage(BasePage):
    _url = "http://www.sberbank.ru/ru/quotes/converter"
    _cookies_warn_close_button = (By.CLASS_NAME, "cookie-warning__close")
    _main_current_buy_rate = (
        By.XPATH,
        "//tr[@class= 'rates-current__table-row']//*[contains(@class,'column_buy')]//*[@class='rates-current__rate-value']")
    _main_current_sell_rate = (
        By.XPATH,
        "//tr[@class= 'rates-current__table-row']//*[contains(@class,'column_sell')]//*[@class='rates-current__rate-value']")
    _amount_input_field = (By.CSS_SELECTOR, ".widget-rates .input input")
    _result_button = (By.CLASS_NAME, "rates-button")
    _from_currency_selector = (By.XPATH, "//*[contains(@class,'converter-from')]//*[@class='select']")
    _to_currency_selector = (By.XPATH, "//*[@name='converterTo']/../*[@class='select']")
    _currency_in_list = "//div[@class='visible']//span[contains(text(),'{}')]"
    _total_from = (By.CLASS_NAME, "rates-converter-result__total-from")
    _total_to = (By.CLASS_NAME, "rates-converter-result__total-to")

    def __init__(self, driver):
        super().__init__(driver)

    @allure.step("Open Sberbank exchange calculator")
    def open(self):
        self.driver.get(self._url)
        try:
            self.driver_wait(5).until(expected_conditions.element_to_be_clickable(self._cookies_warn_close_button))
            self.driver.find_element(*self._cookies_warn_close_button).click()
        except WebDriverException:
            pass

    @allure.step("Get current main  buy rate")
    def get_current_buy_rate(self):
        return self.driver.find_element(*self._main_current_buy_rate).text

    @allure.step("Get current main  sell rate")
    def get_current_sell_rate(self):
        return self.driver.find_element(*self._main_current_sell_rate).text

    def input_exchange_sum(self, text):
        with allure.step("Input exchange sum :" + str(text)):
            input_field = self.driver.find_element(*self._amount_input_field)
            input_field.clear()
            input_field.send_keys(text)

    def choice_from_currency(self, currency):
        with allure.step("Choice from currency: " + str(currency)):
            self.__choice_currency(self._from_currency_selector, currency)

    def choice_to_currency(self, currency):
        with allure.step("Choice to currency: " + str(currency)):
            self.__choice_currency(self._to_currency_selector, currency)

    def __choice_currency(self, list_locator, currency):
        self.driver.find_element(*list_locator).click()
        currency_locator = [By.XPATH, self._currency_in_list.format(currency)]
        self.driver.find_element(*currency_locator).click()

    @allure.step("Press on 'Show result' button")
    def press_on_show_result_button(self):
        button = self.driver.find_element(*self._result_button)
        actions = ActionChains(self.driver)
        actions.move_to_element(button).perform()
        button.click()

    def check_total_result(self, ammount, from_currency, to_currency):
        with allure.step("Check result of exchange: {}{} to {}".format(ammount, from_currency, to_currency)):
            self.driver_wait().until(expected_conditions.presence_of_element_located(self._total_from))
            expected_result_from_api = CurrencyConverter().convert_currency_by_api_rates(ammount, from_currency,
                                                                                         to_currency)
            actual_from_data = self.driver.find_element(*self._total_from).text.replace(" ", "").replace("=", "")
            actual_to_data = self.driver.find_element(*self._total_to).text.replace(" ", "")
            expected_from = ("%.2f" % float(ammount)).replace(".", ",") + from_currency
            expected_to = (str(float(expected_result_from_api)).replace(".", ",")) + to_currency
            assert actual_from_data == expected_from
            assert actual_to_data == expected_to

    def check_rates_in_widget(self, from_currency, to_currency):
        current_buy_rate = self.get_current_buy_rate()
        current_sell_rate = self.get_current_sell_rate()
        expected_rates = ApiHelper().get_current_buy_and_sell_values_from_api(from_currency, to_currency)
        expected_rates[0] = str(expected_rates[0]).replace(".", ",")
        expected_rates[1] = str(expected_rates[1]).replace(".", ",")
        assert expected_rates == [current_buy_rate, current_sell_rate]
