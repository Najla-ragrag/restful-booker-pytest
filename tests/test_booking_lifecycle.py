import requests


def auth_headers(token):
    return {
        "Cookie": f"token={token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def test_update_booking(base_url, token, booking):
    new_data = {
        "firstname": "UpdatedName",
        "lastname": "QA",
        "totalprice": 300,
        "depositpaid": False,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-05"},
        "additionalneeds": "Breakfast",
    }
    response = requests.put(
        f"{base_url}/booking/{booking['id']}", json=new_data, headers=auth_headers(token)
    )
    assert response.status_code == 200
    body = response.json()
    assert body["firstname"] == new_data["firstname"]
    assert body["totalprice"] == 300


def test_partial_update_keeps_other_fields(base_url, token, booking):
    response = requests.patch(
        f"{base_url}/booking/{booking['id']}",
        json={"totalprice": 999},
        headers=auth_headers(token),
    )
    assert response.status_code == 200
    body = response.json()
    assert body["totalprice"] == 999
    assert body["lastname"] == booking["payload"]["lastname"]


def test_delete_booking_then_verify_404(base_url, token, booking):
    url = f"{base_url}/booking/{booking['id']}"
    response = requests.delete(url, headers=auth_headers(token))
    assert response.status_code == 201
    check = requests.get(url, headers={"Accept": "application/json"})
    assert check.status_code == 404


def test_delete_without_token_is_forbidden(base_url, booking):
    url = f"{base_url}/booking/{booking['id']}"
    response = requests.delete(url)
    assert response.status_code == 403
    assert response.text == "Forbidden"
    still_there = requests.get(url, headers={"Accept": "application/json"})
    assert still_there.status_code == 200