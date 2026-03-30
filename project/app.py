from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, model_validator

app = FastAPI()

registered_names = set()
registered_emails = set()


class UserRegistration(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="User's full name"
    )

    email: EmailStr = Field(
        ...,
        description="User's email address"
    )

    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters"
    )

    confirm_password: str = Field(
        ...,
        description="Confirm password"
    )

    @model_validator(mode='after')
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegistration):

    if user.name in registered_names:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    if user.email in registered_emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    registered_names.add(user.name)
    registered_emails.add(user.email)

    return {
        "message": "User registered successfully",
        "registered_user": {
            "name": user.name,
            "email": user.email
        }
    }