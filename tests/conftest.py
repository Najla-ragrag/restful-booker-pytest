import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def token(base_url):
    payload = {"username": "admin", "password": "password123"}
    response = requests.post(f"{base_url}/auth", json=payload)
    assert response.status_code == 200
    return response.json()["token"]


@pytest.fixture
def booking(base_url):
    payload = {
        "firstname": "Tester",
        "lastname": "QA",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-10-15", "checkout": "2026-10-20"},
        "additionalneeds": "Extra bed",
    }
    response = requests.post(
        f"{base_url}/booking", json=payload, headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    return {"id": response.json()["bookingid"], "payload": payload}