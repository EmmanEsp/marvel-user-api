from fastapi import APIRouter, status
from starlette.responses import JSONResponse

from app.schemas.create_user_request import CreateUserRequest
from app.services.user_service import insert_new_user

router = APIRouter()


@router.post("")
def create_user(user: CreateUserRequest):
    new_user = insert_new_user(user=user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=new_user.__dict__)
