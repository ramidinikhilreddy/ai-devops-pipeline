from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserRegister(BaseModel):
    name: str = Field(min_length=1, description="Name of the user, must not be empty")
    email: EmailStr = Field(description="Valid email address of the user")
    password: str = Field(min_length=8, description="Password with a minimum length of 8 characters")


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    # Pydantic's validation (EmailStr, Field(min_length)) automatically handles
    # name not empty, email validity, and password minimum length.
    # If validation fails, FastAPI will automatically return a 422 Unprocessable Entity.

    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }