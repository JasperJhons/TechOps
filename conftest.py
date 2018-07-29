import allure
import pytest
from selenium import webdriver

from utils.csv_reader import read_test_data_from_csv


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser for tests"
    )
    parser.addoption(
        "--fullscreen", action="store", default=True, help="Fullscreen browser mode"
    )


@pytest.yield_fixture(scope="session")
def driver(request):
    default_driver_dir = "./drivers/"
    browser = request.config.getoption("--browser")

    driver = None
    if browser == "chrome":
        driver = webdriver.Chrome(default_driver_dir + "chromedriver")
    else:
        # You can add another browsers here
        pass

    if driver is not None:
        driver.maximize_window()

    yield driver
    driver.quit()


@pytest.mark.tryfirst
def pytest_runtest_makereport(item, call, __multicall__):
    rep = __multicall__.execute()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture(scope="function")
def screenshot_on_failure(request, driver):
    def fin():
        attach = driver.get_screenshot_as_png()
        if request.node.rep_setup.failed:
            allure.attach(request.function.__name__, attach, allure.attach_type.PNG)
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                allure.attach(request.function.__name__, attach, allure.attach_type.PNG)

    request.addfinalizer(fin)


def pytest_generate_tests(metafunc):
    exchange_data = read_test_data_from_csv("exchange_test_data.csv")
    if "ammount" in metafunc.fixturenames or "from_currency" in metafunc.fixturenames:
        metafunc.parametrize("ammount, from_currency, to_currency", exchange_data)
