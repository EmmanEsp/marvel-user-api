from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.infraestructure.mongodb_client import get_client
from app.schemas.create_user_request import CreateUserRequest
from app.schemas.create_user_response import CreateUserResponse


def insert_new_user(user: CreateUserRequest):
    client = get_client()
    db = client.user

    user_exist = db.users.find_one({"email": user.email})

    if user_exist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use.")

    user_encoded = jsonable_encoder(user)
    new_user = db.users.insert_one(user_encoded)

    return CreateUserResponse(id=str(new_user.inserted_id))
