
from __future__ import annotations
from typing import Tuple
import re
import allure
from .client import HttpClient
from ..models.cart import AddToCartResponse, AddToCartRequest
from ..models.auth import LoginRequest

@allure.step("API: login and get auth cookie")
def api_login_and_get_cookie(client: HttpClient, email: str, password: str) -> Tuple[HttpClient, str]:
    client.get("/login")
    login = LoginRequest(Email=email, Password=password, RememberMe="false")
    resp = client.post("/login", data=login.dict(), allow_redirects=False)
    assert resp.status_code in (302, 200)
    cookie_header = "; ".join([f"{c.name}={c.value}" for c in client.s.cookies])
    return client, cookie_header

@allure.step("API: add product to cart")
def api_add_to_cart(client: HttpClient, product_id: int, qty: int = 1) -> AddToCartResponse:
    endpoint = f"/addproducttocart/details/{product_id}/1"
    payload = AddToCartRequest(product_id=product_id, qty=qty)
    r = client.post(endpoint, data=payload.as_form(), headers={"X-Requested-With": "XMLHttpRequest"})
    assert r.status_code in (200, 302)
    data = r.json()
    parsed = AddToCartResponse(**data)
    assert parsed.success is True
    return parsed

@allure.step("API: clear or set qty by product name")
def api_clear_qty(client: HttpClient, product_name: str):
    page = client.get("/cart")
    m = re.search(rf'name="removefromcart\[(\d+)\]".*?class="product-name".*?>\s*{re.escape(product_name)}', page.text, re.S | re.I)
    if m:
        item_id = m.group(1)
        form = {
            f"removefromcart[{item_id}]": "on",
            "updatecart": "Update shopping cart"
        }
        resp = client.post("/cart", data=form)
        assert resp.status_code in (200, 302)

