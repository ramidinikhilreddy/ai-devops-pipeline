from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=2)  # ❌ WRONG ON PURPOSE

@app.post("/register", status_code=status.HTTP_200_OK)  # ❌ WRONG
def register_user(user: UserRegister):
    return {
        "message": "User registered successfully"
    }