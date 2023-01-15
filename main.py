import uvicorn

from fastapi import FastAPI

from typing import Optional

from enum import Enum

app = FastAPI()


# 추가: 현재 유저를 반환하는 앤드포인트
@app.get("/users/me")
def get_current_user():
    return {"user_id": 123}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/users")
def get_users(limit: Optional[int] = None):
    return {"limit": limit}


@app.get("/users2")
def get_users2(is_admin: bool, limit: int = 100):  # 추가: q
    return {"is_admin": is_admin, "limit": limit}  # 추가: q


class UserLevel(str, Enum):
    a = "a"
    b = "b"
    c = "c"

@app.get("/users3")
def get_users3(grade: UserLevel = UserLevel.a):
    return {"grade": grade}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)