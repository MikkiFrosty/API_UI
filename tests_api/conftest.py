import os, pytest
from api_client.client import ApiClient

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("API_BASE_URL", "https://reqres.in/api")

@pytest.fixture(scope="session")
def api_client(base_url: str) -> ApiClient:
    default_headers = {}
    token = os.getenv("API_TOKEN")
    if token:
        default_headers["Authorization"] = f"Bearer {token}"
    x_api_key = os.getenv("X_API_KEY")
    if x_api_key:
        default_headers["x-api-key"] = x_api_key
    return ApiClient(base_url, default_headers=default_headers)
