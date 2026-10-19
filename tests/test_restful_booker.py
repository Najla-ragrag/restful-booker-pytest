import requests

BASE_URL = "https://restful-booker.herokuapp.com"


def test_ping_returns_201():
    response = requests.get(f"{BASE_URL}/ping")
    assert response.status_code == 201


def test_create_token_returns_token():
    payload = {"username": "admin", "password": "password123"}
    response = requests.post(f"{BASE_URL}/auth", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()


def test_create_booking_returns_booking_id():
    payload = {
        "firstname": "Tester",
        "lastname": "QA",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-10-15", "checkout": "2026-10-20"},
        "additionalneeds": "Extra bed",
    }
    response = requests.post(
        f"{BASE_URL}/booking", json=payload, headers={"Accept": "application/json"}
    )
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body["bookingid"], int)
    assert body["booking"]["firstname"] == payload["firstname"]