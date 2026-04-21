from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserRegister(BaseModel):
    name: str
    email: str
    password: str


@app.post("/register")
def register_user(user: UserRegister):
    if len(user.password) < 3:
        return {"error": "password too short"}

    return {
        "msg": "ok",
        "user": user
    }
