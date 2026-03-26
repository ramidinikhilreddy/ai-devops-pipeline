from backend.services.user_service import REGISTERED_USERS, register_user


def setup_function():
    """
    Reset the in-memory store before each test.
    """
    REGISTERED_USERS.clear()


def test_successful_user_registration():
    payload = {
        "name": "Prakriti",
        "email": "prakriti@example.com",
        "password": "secure123",
    }

    result = register_user(payload)

    assert result["status"] == 201
    assert result["body"]["message"] == "User registered successfully."
    assert len(REGISTERED_USERS) == 1
    assert REGISTERED_USERS[0]["email"] == "prakriti@example.com"
    assert REGISTERED_USERS[0]["password"] != "secure123"


def test_missing_required_field():
    payload = {
        "name": "Prakriti",
        "email": "prakriti@example.com",
    }

    result = register_user(payload)

    assert result["status"] == 400
    assert "required" in result["body"]["message"].lower()


def test_invalid_email_format():
    payload = {
        "name": "Prakriti",
        "email": "prakriti-email",
        "password": "secure123",
    }

    result = register_user(payload)

    assert result["status"] == 400
    assert result["body"]["message"] == "Invalid email format."


def test_weak_password():
    payload = {
        "name": "Prakriti",
        "email": "prakriti@example.com",
        "password": "123",
    }

    result = register_user(payload)

    assert result["status"] == 400
    assert "at least 8 characters" in result["body"]["message"]


def test_duplicate_email_registration():
    first_payload = {
        "name": "Prakriti",
        "email": "prakriti@example.com",
        "password": "secure123",
    }

    second_payload = {
        "name": "Another User",
        "email": "prakriti@example.com",
        "password": "anothersecure123",
    }

    first_result = register_user(first_payload)
    second_result = register_user(second_payload)

    assert first_result["status"] == 201
    assert second_result["status"] == 409
    assert second_result["body"]["message"] == "Email already exists."