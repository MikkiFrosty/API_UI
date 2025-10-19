import allure
import json
import allure
from jsonschema import validate
from schemas import create_user, update_user, list_users, single_user, error_schema
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_get_users_list(api_client):
    r = api_client.get("/users", verify=False, params={"page": 2})
    assert r.status_code == 200
    validate(r.json(), list_users)

def test_get_single_user(api_client):
    r = api_client.get("/users/2", verify=False)
    assert r.status_code == 200
    validate(r.json(), single_user)

def test_get_single_user_404(api_client):
    r = api_client.get("/users/23", verify=False)
    assert r.status_code == 404
    assert r.json() == {}

def test_post_create_user_schema_from_file(api_client):
    payload = {"name": "morpheus", "job": "leader"}
    r = api_client.post("/users", verify=False, json_body=payload)
    assert r.status_code == 201
    with open("post_users.json", encoding="utf-8") as f:
        validate(r.json(), create_user)

def test_post_register_missing_password(api_client):
    payload = {"email": "sydney@fife"}
    r = api_client.post("/register", verify=False, json_body=payload)
    assert r.status_code == 400
    validate(r.json(), error_schema)

def test_put_update_user(api_client):
    payload = {"name": "neo", "job": "the one"}
    r = api_client.put("/users/2", verify=False, json_body=payload)
    assert r.status_code == 200
    validate(r.json(), update_user)

def test_delete_user(api_client):
    r = api_client.delete("/users/2", verify=False)
    assert r.status_code == 204
    assert r.text == ""