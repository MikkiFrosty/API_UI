import os
import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(scope='session', autouse=True)
def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-dev-tools')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1366,768')

    browser.config.driver_options = options
    browser.config.base_url = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com')
    browser.config.timeout = 10

    yield
    browser.quit()
