from datetime import datetime, timedelta

import bcrypt
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from jose import jwt

from app.infraestructure.mongodb_client import get_client
from app.schemas.auth_user_request import AuthUserRequest
from app.schemas.create_user_request import CreateUserRequest
from app.schemas.create_user_response import CreateUserResponse
from app.schemas.user_auth_response import UserAuthResponse
from app.settings.security_settings import get_security_settings


def _create_user_jwt(user_id: str):
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode = {"id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(
        to_encode,
        get_security_settings().secret_key,
        algorithm="HS256",
    )
    return encoded_jwt


def _hash_password(password: str):
    pass_encoded = password.encode()
    salt = get_security_settings().secure_keyword
    return bcrypt.hashpw(password=pass_encoded, salt=salt.encode())


def insert_new_user(user: CreateUserRequest):
    client = get_client()
    db = client.user

    user_exist = db.users.find_one({"email": user.email})

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Email {user.email} already in use.")

    user.password = _hash_password(user.password)
    user_encoded = jsonable_encoder(user)
    new_user = db.users.insert_one(user_encoded)

    return CreateUserResponse(id=str(new_user.inserted_id))


def authenticate_user(auth: AuthUserRequest):
    client = get_client()
    db = client.user

    user = db.users.find_one({"email": auth.email})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {auth.email} not found.")

    saved_pass = str(user["password"])

    if not bcrypt.checkpw(auth.password.encode(), saved_pass.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Incorrect user credentials.")

    user_token = _create_user_jwt(str(user["_id"]))

    return UserAuthResponse(
        name=user["name"],
        age=user["age"],
        email=user["email"],
        token=user_token,
    )
