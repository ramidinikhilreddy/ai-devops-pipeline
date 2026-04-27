from pathlib import Path

BROKEN_APP = """from fastapi import FastAPI
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
"""


def main() -> None:
    app_file = Path("project/app.py")
    app_file.parent.mkdir(parents=True, exist_ok=True)
    app_file.write_text(BROKEN_APP, encoding="utf-8")
    print("✅ Reset project/app.py to the intentionally broken demo version.")


if __name__ == "__main__":
    main()