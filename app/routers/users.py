from fastapi import APIRouter, BackgroundTasks, Body, Depends
from pydantic import BaseModel
from typing import Annotated

from ..dependencies import common_parameters

router = APIRouter()  ## you can name the variable whatevern you want
# you can think of the router as mini Fastapi class
# all the methods of the Fastapi class are supported


class User(BaseModel):
    email: str


class UserIn(User):
    password: str


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)
        print("✅ Email Sent")


@router.get("/users/profile")
def profile(user: UserIn) -> User:
    return user


@router.post("/users/email")
def send_email(
    email: Annotated[str, Body(embed=True)], background_tasks: BackgroundTasks
):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"detail": f"Email Sent to {email}"}


@router.get("/users/secret")
def tell_secret(commons: Annotated[dict, Depends(common_parameters)]):
    print(f"✅ {commons}")
    return {"secret": "Some top level secret"}
