# restful-booker-pytest
# Restful-Booker API Tests in Python (pytest)

![Pytest API Tests](https://github.com/Najla-ragrag/restful-booker-pytest/actions/workflows/pytest.yml/badge.svg)

Code-based API tests for the public [Restful-Booker](https://restful-booker.herokuapp.com/apidoc/index.html) booking API, written with **Python, requests and pytest** and run automatically with **GitHub Actions**.

This is the code version of my Postman project, [restful-booker-api-testing](https://github.com/Najla-ragrag/restful-booker-api-testing). The Postman suite explores and documents the API; this one covers the same behaviour as maintainable, version-controlled Python tests.

## Results

| Run | Tests | Failed |
|-----|-------|--------|
| pytest, GitHub Actions | 16 | 0 |

A JUnit XML report is uploaded as a build artifact on every run.

## What is tested

| File | Tests | Covers |
|------|-------|--------|
| `tests/test_restful_booker.py` | 3 | Ping (201), create token, create booking |
| `tests/test_booking_lifecycle.py` | 4 | Update (PUT), partial update (PATCH), delete then verify 404, delete without a token |
| `tests/test_negative.py` | 9 | Bad credentials (3 cases) and PUT/PATCH/DELETE with no token or an invalid token (6 cases) |

### Parametrized tests

Data-driven tests use `@pytest.mark.parametrize`, so one test function runs once per data row and each case is reported by name.

- **Bad credentials:** `wrong password`, `wrong username`, `both wrong`. Each returns 200 with `{"reason": "Bad credentials"}` and no token.
- **Write requests without a valid token:** `PUT`, `PATCH`, `DELETE` combined with `no token` and `invalid token` (6 cases). Each returns 403, and the test then checks that the booking still exists and is unchanged.

### Fixtures

Shared setup lives in `tests/conftest.py`:

- `base_url`: the API address
- `token`: created once per test session
- `booking`: a fresh booking created for each test that needs one, so tests do not depend on each other or on existing data

## Observations

The API resets its data regularly and is shared by everyone, so every test creates its own data.

- A wrong password **or** a wrong username returns **200** with `Bad credentials`, not 401.
- `PUT`, `PATCH` and `DELETE` with no token or an invalid token all return **403**, and the booking is left unchanged.
- A successful delete returns **201**, followed by 404 when the booking is requested again.

See the [Postman project](https://github.com/Najla-ragrag/restful-booker-api-testing) for the full list of findings, including a likely bug (500 when required fields are missing).

## Project structure

```
.
├── .github/workflows/pytest.yml
├── requirements.txt
└── tests/
    ├── conftest.py
    ├── test_restful_booker.py
    ├── test_booking_lifecycle.py
    └── test_negative.py
```

## Run locally

```bash
pip install -r requirements.txt
pytest -v
```

## CI/CD

`.github/workflows/pytest.yml` runs on every push to `main` (or manually from the Actions tab). It checks out the repo, sets up Python 3.12, installs the dependencies, runs `pytest -v` and uploads the JUnit report.

## Skills demonstrated

- API test automation in Python with `requests` and `pytest`
- Fixtures with different scopes for token and test-data setup
- Data-driven testing with `parametrize`
- Positive and negative test design, including checks that rejected requests do not change data
- Independent, repeatable tests on a shared public API
- CI/CD with GitHub Actions
