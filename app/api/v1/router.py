from fastapi import APIRouter, status

from app.api.v1.endpoints import users

v1_api_router = APIRouter()

v1_api_router.include_router(
    users.router,
    tags=["Users"],
    prefix="/users",
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)
