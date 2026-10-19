import pytest
import requests


@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "wrongpass"),
        ("wronguser", "password123"),
        ("wronguser", "wrongpass"),
    ],
    ids=["wrong password", "wrong username", "both wrong"],
)
def test_auth_with_bad_credentials(base_url, username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{base_url}/auth", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["reason"] == "Bad credentials"
    assert "token" not in body


@pytest.mark.parametrize("method", ["put", "patch", "delete"])
@pytest.mark.parametrize(
    "cookie", [None, "token=invalidtoken123"], ids=["no token", "invalid token"]
)
def test_write_requests_without_valid_token_are_forbidden(
    base_url, booking, method, cookie
):
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if cookie:
        headers["Cookie"] = cookie
    url = f"{base_url}/booking/{booking['id']}"

    response = requests.request(method, url, json={"totalprice": 1}, headers=headers)
    assert response.status_code == 403

    # the booking must be unchanged and still exist
    check = requests.get(url, headers={"Accept": "application/json"})
    assert check.status_code == 200
    assert check.json()["totalprice"] == booking["payload"]["totalprice"]