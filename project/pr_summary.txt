from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

users = set()

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

@app.post("/register")
def register(payload: RegisterRequest):
    if payload.email in users:
        raise HTTPException(status_code=400, detail="Email already exists")
    users.add(payload.email)
    return {"message": "User registered successfully"}