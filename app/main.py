from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["OPTIONS", "GET"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"message": "Hello World"}