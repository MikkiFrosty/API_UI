import os
import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope='session', autouse=True)
def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1366,768')

    cache_path = os.getenv('WDM_CACHE', '.wdm-cache')
    os.makedirs(cache_path, exist_ok=True)

    driver_path = ChromeDriverManager(path=cache_path, cache_valid_range=0).install()
    service = Service(driver_path)
    browser.config.driver = webdriver.Chrome(service=service, options=options)

    browser.config.base_url = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com')
    browser.config.timeout = 10

    yield
    browser.quit()
