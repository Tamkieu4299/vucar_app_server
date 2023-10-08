from datetime import date
from typing import Optional, Union

from pydantic import  BaseModel


class UserBaseSchema(BaseModel):
    user_id: int
    name: str
    password: str

    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    user_id: int
    name: str
    authority_id: int
    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    authority_id: str
    class Config:
        orm_mode = True
