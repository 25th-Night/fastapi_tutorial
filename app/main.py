import time

from typing import Optional
from fastapi import BackgroundTasks, FastAPI, status

app = FastAPI()


def write_log(message: str):
    time.sleep(2.0)

    with open("log.txt", mode="a") as log:
        log.write(message)


@app.post("/send-notification/{email}", status_code=status.HTTP_202_ACCEPTED)
async def send_notification(email: str, background_tasks: BackgroundTasks):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)

    return {"message": "Message sent"}