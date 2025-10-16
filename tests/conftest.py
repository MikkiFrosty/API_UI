
import os
import pytest
from selene import browser
from api_ui_cart_project.api.client import HttpClient

@pytest.fixture(scope="session", autouse=True)
def base_url():
    browser.config.base_url = os.getenv("BASE_URL", "https://demowebshop.tricentis.com")
    return browser.config.base_url

@pytest.fixture(scope="session")
def client(base_url):
    return HttpClient(base_url=base_url)
