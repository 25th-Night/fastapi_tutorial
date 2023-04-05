from typing import List

from fastapi import Depends, FastAPI, HTTPException, Form, File, UploadFile
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from tempfile import NamedTemporaryFile
from typing import IO

from . import models, schemas
from .database import SessionLocal, engine


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