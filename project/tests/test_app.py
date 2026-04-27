from fastapi.testclient import TestClient
from project.app import app, users

client = TestClient(app)


def setup_function():
    users.clear()


def test_register_success():
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        },
    )
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"


def test_register_invalid_email():
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "invalid-email",
            "password": "password123"
        },
    )
    assert response.status_code == 422


def test_register_short_password():
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": "shortpass@example.com",
            "password": "123"
        },
    )
    assert response.status_code == 422


def test_register_duplicate_email():
    payload = {
        "name": "Dup User",
        "email": "dup@example.com",
        "password": "password123"
    }

    first = client.post("/register", json=payload)
    second = client.post("/register", json=payload)

    assert first.status_code == 200
    assert second.status_code == 400
    assert second.json()["detail"] == "Email already exists"


def test_register_missing_name():
    response = client.post(
        "/register",
        json={
            "email": "missingname@example.com",
            "password": "password123"
        },
    )
    assert response.status_code == 422