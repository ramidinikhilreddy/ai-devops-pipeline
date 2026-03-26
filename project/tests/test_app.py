from fastapi.testclient import TestClient
from project.app import app

client = TestClient(app)

def test_successful_registration():
    response = client.post("/register", json={
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "strongpassword123"
    })
    assert response.status_code == 201

def test_invalid_email_format():
    response = client.post("/register", json={
        "name": "Jane",
        "email": "invalid",
        "password": "strongpassword123"
    })
    assert response.status_code == 422

def test_password_too_short():
    response = client.post("/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "short"
    })
    assert response.status_code == 422
