from pydantic import BaseModel
# from typing import Optional


class UserSchema(BaseModel):
    id: int | None = None
    name: str
    username: str
    user_passw: str


class UpdateUsername(BaseModel):
    username: str
    user_passw: str


class dataUser(BaseModel):
    username: str
    user_passw: str
