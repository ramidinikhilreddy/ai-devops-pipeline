from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()


class UserRegister(BaseModel):
    name: str = Field(min_length=1, description="Name must not be empty")
    email: EmailStr
    password: str = Field(min_length=8, description="Password must be at least 8 characters long")


@app.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }