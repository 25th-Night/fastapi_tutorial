import uvicorn

from fastapi import FastAPI

app = FastAPI()


# 현재 유저를 반환하는 앤드포인트
@app.get("/users/me")
def get_current_user():
    return {"user_id": 123}

# 변수로 입력받는 엔드포인트가 밑에 위치해야 함
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)