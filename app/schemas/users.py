from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """ Return response data """
    id: int
    email: EmailStr
    name: str


class UserCreate(BaseModel):
    """ Validate request data """
    email: EmailStr
    name: str
    password: str


class User(UserBase):
    """ Return detailed response data with token """
    token = {}