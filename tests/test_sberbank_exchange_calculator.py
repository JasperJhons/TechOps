import pytest

from pages.exchange_calculator_page import ExchangeCalculatorPage


@pytest.mark.usefixtures("screenshot_on_failure")
def test_exchange_calculator_with_default_params(driver, ammount, from_currency, to_currency):
    sberbank = ExchangeCalculatorPage(driver)
    sberbank.open()
    sberbank.input_exchange_sum(ammount)
    sberbank.choice_from_currency(from_currency)
    sberbank.choice_to_currency(to_currency)
    sberbank.press_on_show_result_button()
    sberbank.check_total_result(ammount, from_currency, to_currency)


@pytest.mark.usefixtures("screenshot_on_failure")
def test_exchange_calculator_rates_widget(driver, ammount, from_currency, to_currency):
    sberbank = ExchangeCalculatorPage(driver)
    sberbank.open()
    sberbank.choice_from_currency(from_currency)
    sberbank.choice_to_currency(to_currency)
    sberbank.check_rates_in_widget(from_currency, to_currency)
