import os
import requests
import urllib3
from selene import browser, have

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE = os.getenv('BASE_URL', 'https://demowebshop.tricentis.com')
EMAIL = os.getenv('EMAIL', 'example12000@example.com')
PASSWORD = os.getenv('PASSWORD', '123456')

def test_requests_session():
    s = requests.Session()
    s.trust_env = False
    s.proxies = {'http': None, 'https': None}
    s.verify = False
    return s

def test_api_login(session):
    r = session.post(f"{BASE}/login",
                     data={'Email': EMAIL, 'Password': PASSWORD, 'RememberMe': False},
                     allow_redirects=False)
    assert r.status_code in (200, 302)
    return r

def test_api_add_to_cart(session, product_id: int, qty: int = 1):
    payload = {f'addtocart_{product_id}.EnteredQuantity': str(qty)}
    r = session.post(f"{BASE}/addproducttocart/catalog/{product_id}/1", data=payload, allow_redirects=False)
    if r.status_code >= 400:
        r = session.post(f"{BASE}/addproducttocart/details/{product_id}/1", data=payload, allow_redirects=False)
    assert r.status_code in (200, 302)
    return r

def test_transfer_cookies_to_browser(session):
    browser.open('/')
    for c in session.cookies:
        try:
            browser.driver.execute_cdp_cmd('Network.setCookie', {
                'name': c.name, 'value': c.value, 'domain': c.domain or 'demowebshop.tricentis.com',
                'path': c.path or '/', 'httpOnly': False, 'secure': False
            })
        except Exception:
            try:
                browser.driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path or '/'})
            except Exception:
                pass

def test_add_item_via_api_and_check_cart_ui():
    s = test_requests_session()
    test_api_login(s)
    test_api_add_to_cart(s, product_id=31, qty=1)

    test_transfer_cookies_to_browser(s)

    browser.open('/cart')
    browser.element('#shopping-cart-form').should(have.text('Health'))
