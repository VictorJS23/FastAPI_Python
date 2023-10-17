from fastapi import APIRouter, Response
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_200_OK
from schema.user_schema import UserSchema, UpdateUsername, dataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List

user = APIRouter()


@user.get("/")
def root():
    return {"message": "Hi, I am FastAPI with a router"}


@user.get("/api/user", response_model=List[UserSchema])
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()

        return result


@user.get("/api/user/{user_id}", response_model=UserSchema)
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()

        return result


@user.post("/api/user", status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(
            data_user.user_passw, "pbkdf2:sha256:30", 30)

        conn.execute(users.insert().values(new_user))

    return Response(status_code=HTTP_201_CREATED)


@user.post("/api/user/login")
def user_login(data_user: dataUser, status_code=HTTP_200_OK):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.username == data_user.username)).first()

        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_passw)

            if (check_passw):
                return {
                    "status": HTTP_200_OK,
                    "message": "Access succes"
                }
            return {
                "status": HTTP_401_UNAUTHORIZED,
                "message": "Access denied"
            }


@user.put("/api/user/{user_id}")
def update_user(user_id: int, data: UpdateUsername):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(
            users.c.id == user_id)).first()

        if result != None:
            encryp_passw = generate_password_hash(
                data.user_passw, "pbkdf2:sha256:30", 30)
            conn.execute(users.update().values(username=data.username,
                         user_passw=encryp_passw).where(users.c.id == user_id))
            return result
        return {
            "detail": "Usuario no encontrado"
        }


@user.delete("/api/user/{user_id}", status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id: str):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))

        return Response(status_code=HTTP_204_NO_CONTENT)
