import uvicorn

from fastapi import FastAPI, status

from pydantic import BaseModel, HttpUrl

app = FastAPI()


class User(BaseModel):
    name: str
    avatar_url: HttpUrl = "https://icotar.com/avatar/fastcampus.png?s=200"


class CreateUser(User):
    password: str


# @app.post("/users", response_model=User, status_code=201)  # 추가: status_code
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)  # 추가: status_code
def create_user(user: CreateUser):
    return user

# -----------------------------------------------


# class User(BaseModel):
#     name: str = "fastapi"
#     password: str
#     avatar_url: HttpUrl = None


# @app.post(
#     "/include",
#     response_model=User,
#     response_model_include={"name", "avatar_url"},  # Set 타입. List도 괜찮습니다.
# )
# def get_user_with_include(user: User):
#     return user


# @app.post(
#     "/exclude",
#     response_model=User,
#     response_model_exclude={"password"},
# )
# def get_user_with_exclude(user: User):
#     return user


# @app.post(
#     "/unset",
#     response_model=User,
#     response_model_exclude_unset=True,
# )
# def get_user_with_exclude_unset(user: User):
#     return user


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)