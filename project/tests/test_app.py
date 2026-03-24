import pytest
from fastapi.testclient import TestClient
from project.app import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def has_field_error(detail_list, field_name):
    return any(field_name in error.get("loc", []) for error in detail_list)


def test_successful_registration(client):
    response = client.post("/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "strongpassword123"
    })

    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "User registered successfully"
    assert body["registered_user"]["name"] == "John Doe"
    assert body["registered_user"]["email"] == "john.doe@example.com"


def test_invalid_email_format(client):
    response = client.post("/register", json={
        "name": "Jane Smith",
        "email": "jane.smith@invalid",
        "password": "securepassword456"
    })

    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert has_field_error(body["detail"], "email")


def test_password_too_short(client):
    response = client.post("/register", json={
        "name": "Alice Wonderland",
        "email": "alice@example.com",
        "password": "short"
    })

    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert has_field_error(body["detail"], "password")


def test_missing_name(client):
    response = client.post("/register", json={
        "name": "",
        "email": "missingname@example.com",
        "password": "validpassword123"
    })

    assert response.status_code == 422
    body = response.json()
    assert "detail" in body
    assert has_field_error(body["detail"], "name")
