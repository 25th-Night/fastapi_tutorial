from typing import List, Any, Optional, Dict

from fastapi import Depends, FastAPI, HTTPException, Form, File, UploadFile, HTTPException, status, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from tempfile import NamedTemporaryFile
from typing import IO

from . import models, schemas
from .database import SessionLocal, engine

from fastapi.responses import JSONResponse


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existed_user = db.query(models.User).filter_by(
        email=user.email
    ).first()

    if existed_user:
        raise HTTPException(status_code=400, detail="Email already registerd")

    user = models.User(email=user.email, password=user.password)
    db.add(user)
    db.commit()

    return user


@app.get("/users", response_model=List[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return db.query(models.User).all() 


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


@app.post("/file/size")
def get_filesize(file: bytes = File(...)):
    return {"file_size": len(file)}


# @app.post("/file/info")
# def get_file_info(file: UploadFile = File(...)):
#     return {
#         "content_type": file.content_type,
#         "filename": file.filename
#     }


@app.post("/file/info")
async def get_file_info(file: UploadFile = File(...)):
    file_like_obj = file.file
    contents = await file.read()

    return {
        "content_type": file.content_type,
        "filename": file.filename,
    }


async def save_file(file: IO):
    # s3 업로드라고 생각해 봅시다. delete=True(기본값)이면
    # 현재 함수가 닫히고 파일도 지워집니다.
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name


@app.post("/file/store")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    return {"filepath": path}


users = {
    1: {"name": "Fast"},
    2: {"name": "Campus"},
    3: {"name": "API"},
}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    if user_id not in users.keys():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"<User: {user_id}> is not exists.",
        )
    return users[user_id]


# 방법 1. 파이썬 내장 Exception 클래스를 상속받아 정의
# class SomeError(Exception):
#     def __init__(self, name: str, code: int):
#         self.name = name
#         self.code = code

#     def __str__(self):
#         return f"<{self.name}> is occured. code: <{self.code}>"
    

# # 추가
# @app.exception_handler(SomeError)
# async def some_error_handler(request: Request, exc: SomeError):
#     return JSONResponse(
#         content={"message": f"error is {exc.name}"}, status_code=exc.code
#     )


# @app.get("/error")
# async def get_error():
#     raise SomeError("Hello", 500)


# 방법 2. FastAPI 내장 HTTPException 클래스를 상속받아 정의
class SomeFastAPIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            status_code=status_code, detail=detail, headers=headers
        )


@app.get("/error")
async def get_error():
    raise SomeFastAPIError(500, "Hello")