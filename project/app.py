from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()


class UserRegister(BaseModel):
    name: str = Field(min_length=1)  # Name must not be empty
    email: EmailStr  # Email must be valid
    password: str = Field(min_length=8)  # Password minimum length must be 8


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    # Pydantic validation (name not empty, valid email, password min_length=8)
    # automatically handles 422 responses for invalid input.
    # The manual password length check is no longer needed.

    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }