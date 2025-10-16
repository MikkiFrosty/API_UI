from __future__ import annotations
import requests
import allure
from typing import Optional, Dict, Any
from ..utils.logger import get_logger

INSECURE_HOSTS = ("demowebshop.tricentis.com", "reqres.in")

class HttpClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.s = requests.Session()
        self.log = get_logger("api_ui")

    def _attach(self, name: str, content: str):
        try:
            allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)
        except Exception:
            pass

    def request(self, method: str, endpoint: str, **kwargs):
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = f"{self.base_url}{endpoint}"
        self.log.info(f"{method} {url}")
        self._attach("request", f"METHOD: {method}\nURL: {url}\nKWARGS: {kwargs}")

        # If verify wasn't provided, disable SSL only for known demo/external hosts
        if "verify" not in kwargs:
            if any(h in self.base_url for h in INSECURE_HOSTS):
                kwargs["verify"] = False

        r = self.s.request(method, url, **kwargs)
        self.log.info(f"status={r.status_code} url={r.url}")
        self._attach("response", f"STATUS: {r.status_code}\nURL: {r.url}\nBODY: {r.text[:2000]}")
        return r

    def get(self, endpoint: str, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
