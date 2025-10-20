import os
import allure
from selene import browser, have
from api_ui_cart_project.api.client import HttpClient
from api_ui_cart_project.api.demowebshop_flows import api_login_and_get_cookie, api_add_to_cart, api_clear_qty
from api_ui_cart_project.models.cart import AddToCartResponse

browser.config.timeout = 10

EMAIL = os.getenv("EMAIL", "test@tast.ru")
PASSWORD = os.getenv("PASSWORD", "Qwerty123")

@allure.feature("Авторизация")
def test_api_login_and_cookie():
    client = HttpClient(os.getenv("BASE_URL", "https://demowebshop.tricentis.com"))
    c, cookie = api_login_and_get_cookie(client, EMAIL, PASSWORD)
    assert cookie

@allure.feature("Корзина")
def test_add_to_cart_api_response_schema():
    client = HttpClient(os.getenv("BASE_URL", "https://demowebshop.tricentis.com"))
    resp = api_add_to_cart(client, product_id=31, qty=1)
    assert isinstance(resp, AddToCartResponse)
    assert resp.success is True
    assert "(" in resp.updatetopcartsectionhtml  # например, "(1)"

@allure.feature("Корзина")
def test_clear_cart_api_then_ui_empty():
    client = HttpClient(os.getenv("BASE_URL", "https://demowebshop.tricentis.com"))
    api_add_to_cart(client, product_id=31, qty=1)
    api_clear_qty(client, "14.1-inch Laptop")

    browser.open("/cart")
    browser.element(".order-summary-content").with_(timeout=10).should(have.text("Your Shopping Cart is empty!"))

@allure.feature("Корзина")
def test_add_to_cart_then_ui_shows_item():
    client = HttpClient(os.getenv("BASE_URL", "https://demowebshop.tricentis.com"))
    c, cookie = api_login_and_get_cookie(client, EMAIL, PASSWORD)
    api_add_to_cart(client, product_id=31, qty=1)

    browser.open("/")
    for c in client.s.cookies:
        browser.driver.add_cookie({"name": c.name, "value": c.value, "path": c.path, "domain": c.domain})

    with allure.step("UI: корзина содержит 14.1-inch Laptop"):
        browser.open("/cart")
        browser.element("a.product-name").with_(timeout=10).should(have.exact_text("14.1-inch Laptop"))

