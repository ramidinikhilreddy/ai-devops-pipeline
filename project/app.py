from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
# re module is no longer needed since custom regex validation for password complexity is removed.
# import re # Removed as not used anymore

app = FastAPI()

# In-memory storage for registered users to simulate uniqueness
# In a real application, this would be a database check
registered_users_db = []

class UserRegister(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=20,
        # Modified pattern to allow spaces, as per the failing test case "John Doe"
        # and to align with the "VALIDATION RULES" which only state "name must not be empty".
        # This makes the successful registration test pass.
        pattern=r"^[a-zA-Z0-9 ]+$",
        json_schema_extra={"example": "newuser123"},
        description="Unique identifier for the user account. Must be alphanumeric or contain spaces, 3-20 characters long."
    )
    email: EmailStr = Field(
        ...,
        json_schema_extra={"example": "newuser@example.com"},
        description="Unique email address for the user, used for login and communication. Must be a valid email format."
    )
    password: str = Field(
        ...,
        min_length=8,
        json_schema_extra={"example": "Password123!"},
        # Updated description to reflect validation rules.
        description="Secure password for the user account. Must be at least 8 characters long."
    )

    # Removed the @field_validator('password') `validate_password_complexity` method.
    # This aligns with the "VALIDATION RULES" provided, which explicitly state
    # "password min length = 8" as the only password validation rule, and enables
    # the 'test_successful_registration' to pass with the password "strongpassword123".
    # The `min_length=8` in the Field definition handles the required length validation.


@app.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=dict,
    responses={
        status.HTTP_201_CREATED: {
            "description": "User registered successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "User registered successfully",
                        "registered_user": {
                            "name": "john_doe",
                            "email": "john.doe@example.com"
                        }
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "User with this email or username already exists.",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists."}
                }
            },
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: { # Pydantic validation errors typically result in 422
            "description": "Validation failed",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "password"],
                                "msg": "Password must be at least 8 characters long.",
                                "type": "string_too_short"
                            }
                        ]
                    }
                }
            },
        },
    }
)
async def register_user(user: UserRegister):
    # Simulate uniqueness check
    for existing_user in registered_users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists."
            )
        # Note: The UserRegister model uses 'name', not 'username'.
        if existing_user["name"] == user.name:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this name already exists."
            )

    # In a real application, you would hash the password
    # For this exercise, we store user details directly
    registered_users_db.append({"name": user.name, "email": user.email, "password": user.password})

    # CRITICAL: Response MUST be EXACTLY the specified JSON
    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }