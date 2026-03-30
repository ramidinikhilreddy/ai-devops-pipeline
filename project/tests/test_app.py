from fastapi.testclient import TestClient
from project.app import app

client = TestClient(app)

def test_password_too_short():
    response = client.post("/register", json={
        "name": "Alice",
        "email": "alice@example.com",
        "password": "short"
    })
    assert response.status_code == 422
