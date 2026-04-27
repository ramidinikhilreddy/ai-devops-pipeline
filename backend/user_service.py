from typing import Dict

import hashlib

from backend.utils.validators import is_strong_password, is_valid_email

# Simulated in-memory user store for prototype use.
REGISTERED_USERS = []


def email_exists(email: str) -> bool:
    """
    Check whether a user with the given email already exists.
    """
    normalized_email = email.strip().lower()
    return any(user["email"] == normalized_email for user in REGISTERED_USERS)


def hash_password(password: str) -> str:
    """
    Hash the password using bcrypt.
    """
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def register_user(data: Dict) -> Dict:
    """
    Register a new user after validating the input.
    """
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not name or not email or not password:
        return {
            "status": 400,
            "body": {"message": "Name, email, and password are required."},
        }

    if not is_valid_email(email):
        return {
            "status": 400,
            "body": {"message": "Invalid email format."},
        }

    if not is_strong_password(password):
        return {
            "status": 400,
            "body": {"message": "Password must be at least 8 characters long."},
        }

    if email_exists(email):
        return {
            "status": 409,
            "body": {"message": "Email already exists."},
        }

    hashed_password = hash_password(password)

    REGISTERED_USERS.append(
        {
            "name": name,
            "email": email,
            "password": hashed_password,
        }
    )

    return {
        "status": 201,
        "body": {"message": "User registered successfully."},
    }