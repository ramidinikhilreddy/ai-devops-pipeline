import re


def is_valid_email(email: str) -> bool:
    """
    Validate email format using a simple regex.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def is_strong_password(password: str) -> bool:
    """
    Basic password strength check.
    """
    return len(password) >= 8