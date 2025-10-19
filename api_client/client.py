import time, json, requests, allure

class ApiClient:
    def __init__(self, base_url: str, default_headers: dict | None = None):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.default_headers = default_headers or {}

    def _attach(self, name: str, content: str, attachment_type=allure.attachment_type.TEXT):
        try:
            allure.attach(content, name=name, attachment_type=attachment_type)
        except Exception:
            pass

    def request(self, method: str, endpoint: str, *, params=None, json_body=None, headers=None, **kwargs):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        req_headers = dict(self.default_headers)
        if headers:
            req_headers.update(headers)

        try:
            req_dump = {
                "method": method.upper(),
                "url": url,
                "headers": req_headers,
                "params": params or {},
                "json": json_body,
            }
            self._attach("request", json.dumps(req_dump, ensure_ascii=False, indent=2), allure.attachment_type.JSON)
        except Exception:
            pass

        start = time.time()
        resp = self.session.request(method=method.upper(), url=url, params=params, json=json_body, headers=req_headers, **kwargs)
        elapsed_ms = int((time.time() - start) * 1000)

        try:
            try:
                body_text = json.dumps(resp.json(), ensure_ascii=False, indent=2)
                att_type = allure.attachment_type.JSON
            except Exception:
                body_text = resp.text
                att_type = allure.attachment_type.TEXT

            meta = {"status_code": resp.status_code, "elapsed_ms": elapsed_ms, "headers": dict(resp.headers)}
            self._attach("response-meta", json.dumps(meta, ensure_ascii=False, indent=2), allure.attachment_type.JSON)
            self._attach("response-body", body_text, att_type)
        except Exception:
            pass

        print(f"[API] {method.upper()} {url} -> {resp.status_code} ({elapsed_ms} ms)")
        return resp

    def get(self, endpoint: str, **kw):    return self.request("GET", endpoint, **kw)
    def post(self, endpoint: str, **kw):   return self.request("POST", endpoint, **kw)
    def put(self, endpoint: str, **kw):    return self.request("PUT", endpoint, **kw)
    def delete(self, endpoint: str, **kw): return self.request("DELETE", endpoint, **kw)
