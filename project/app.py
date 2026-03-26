from fastapi import FastAPI, status
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

class UserRegister(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    password: str = Field(..., min_length=8)

@app.post("/register", status_code=201)
def register_user(user: UserRegister):
    return {"message": "User registered successfully", "registered_user": {"name": user.name, "email": user.email}}
