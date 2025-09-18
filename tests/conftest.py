import os
from selene import browser

BASE_URL = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com')

def pytest_sessionstart(session):
    browser.config.base_url = BASE_URL
    browser.config.window_width = 1200
    browser.config.window_height = 900
    browser.config.timeout = 8

def pytest_sessionfinish(session, exitstatus):
    try:
        browser.quit()
    except Exception:
        pass
