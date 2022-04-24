from pydantic import BaseModel


class UserAuthResponse(BaseModel):

    name: str
    age: int
    email: str
    token: str
