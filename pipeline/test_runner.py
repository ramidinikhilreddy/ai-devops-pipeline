import json
import os
import subprocess
import sys


def ensure_directories():
    os.makedirs("project", exist_ok=True)
    os.makedirs("project/tests", exist_ok=True)


def save_file(path: str, content: str):
    with open(path, "w") as f:
        f.write(content)


def get_requirement_json() -> dict:
    return {
        "feature_name": "User Registration API",
        "description": "Create an API endpoint to register a new user using their name, email, and password.",
        "inputs": [
            {"name": "name", "type": "string", "description": "User's full name"},
            {"name": "email", "type": "string", "description": "User's email address"},
            {"name": "password", "type": "string", "description": "User's chosen password"},
        ],
        "validations": [
            {"field": "email", "rule": "Must be a valid email format."},
            {"field": "password", "rule": "Must be at least 8 characters long."},
            {"field": "name", "rule": "Must not be empty."},
        ],
        "expected_output": (
            "Return a success response if registration is valid. "
            "Return an error response if any validation fails."
        ),
        "test_cases": [
            {
                "scenario": "Successful user registration",
                "input": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "password": "strongpassword123",
                },
                "expected_result": "Success response",
            },
            {
                "scenario": "Registration with invalid email format",
                "input": {
                    "name": "Jane Smith",
                    "email": "jane.smith@invalid",
                    "password": "securepassword456",
                },
                "expected_result": "Error response: Invalid email format",
            },
            {
                "scenario": "Registration with password less than 8 characters",
                "input": {
                    "name": "Alice Wonderland",
                    "email": "alice@example.com",
                    "password": "short",
                },
                "expected_result": "Error response: Password must be at least 8 characters",
            },
            {
                "scenario": "Registration with missing name",
                "input": {
                    "name": "",
                    "email": "missingname@example.com",
                    "password": "validpassword123",
                },
                "expected_result": "Error response: Name cannot be empty",
            },
        ],
    }


def get_app_code() -> str:
    return '''from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="User Registration API",
    description="API to register new users with name, email, and password."
)

class UserRegister(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        description="User's full name. Must not be empty."
    )
    email: EmailStr = Field(
        ...,
        description="User's email address. Must be a valid email format."
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User's chosen password. Must be at least 8 characters long."
    )

@app.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    response_description="User successfully registered."
)
async def register_user(user: UserRegister):
    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }
'''


def get_test_code() -> str:
    return '''import pytest
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
'''


def run_pytest():
    print("\\nRUNNING PYTEST...\\n")

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "project/tests/test_app.py", "-v"],
        capture_output=True,
        text=True
    )

    print("PYTEST STDOUT:\\n")
    print(result.stdout)

    if result.stderr:
        print("\\nPYTEST STDERR:\\n")
        print(result.stderr)

    if result.returncode == 0:
        print("\\nALL TESTS PASSED ✅")
    else:
        print("\\nTESTS FAILED ❌")

    return result.returncode, result.stdout, result.stderr


def main():
    ensure_directories()

    requirement = get_requirement_json()
    app_code = get_app_code()
    test_code = get_test_code()

    print("\\nREQUIREMENT JSON:\\n")
    print(json.dumps(requirement, indent=2))

    save_file("project/requirement.json", json.dumps(requirement, indent=2))
    print("\\nRequirement saved to project/requirement.json")

    save_file("project/app.py", app_code)
    print("\\nCode saved to project/app.py")

    save_file("project/tests/test_app.py", test_code)
    print("\\nTests saved to project/tests/test_app.py")

    returncode, stdout, stderr = run_pytest()

    logs = {
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
    }
    save_file("project/test_results.json", json.dumps(logs, indent=2))
    print("\\nPytest logs saved to project/test_results.json")


if __name__ == "__main__":
    main()