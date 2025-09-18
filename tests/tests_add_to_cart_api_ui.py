import os
import requests
import urllib3
from selene import browser, have
import allure
from allure_commons.types import AttachmentType

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com')
LOGIN = os.getenv('EMAIL', 'example12000@example.com')
PASSWORD = os.getenv('PASSWORD', '123456')


def api_login_and_get_cookie():
    with allure.step("Login with API"):
        s = requests.Session()
        s.trust_env = False
        s.verify = False
        result = s.post(
            url=f"{BASE}/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(str(result.status_code), name="Status", attachment_type=AttachmentType.TEXT)
        allure.attach(str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT)
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")
        assert cookie, "Auth cookie is empty"
        return s, cookie


def api_add_to_cart(session: requests.Session, product_id: int, qty: int = 1):
    with allure.step(f"Add product via API: id={product_id}, qty={qty}"):
        res = session.post(
            url=f"{BASE}/addproducttocart/details/{product_id}/1",
            data={"addtocart_{0}.EnteredQuantity".format(product_id): str(qty)},
            allow_redirects=True
        )
        allure.attach(str(res.status_code), name="AddToCart Status", attachment_type=AttachmentType.TEXT)
        try:
            allure.attach(res.text[:1000], name="AddToCart Body (truncated)", attachment_type=AttachmentType.TEXT)
        except Exception:
            pass
        assert res.status_code < 500, "Server error on add to cart"


def transfer_cookies_to_browser(cookie: str):
    with allure.step("Set cookie from API to browser"):
        browser.open('/')  # open domain first due to Selenium requirement
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')


def test_login_through_api_ui():
    s, cookie = api_login_and_get_cookie()
    transfer_cookies_to_browser(cookie)
    with allure.step("Verify successful authorization on UI"):
        browser.element(".account").should(have.text(LOGIN))


def test_add_item_via_api_and_check_cart_ui():
    s, cookie = api_login_and_get_cookie()
    api_add_to_cart(s, product_id=31, qty=1)
    transfer_cookies_to_browser(cookie)
    with allure.step("Open cart and verify item present"):
        browser.open('/cart')
        browser.element('#shopping-cart-form').should(have.text('Health'))
