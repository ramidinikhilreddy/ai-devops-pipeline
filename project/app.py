from fastapi import FastAPI, status
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
        min_length=2,
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
