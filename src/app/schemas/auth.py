from typing import Optional

from pydantic import BaseModel


class RegisterBaseSchema(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class LoginBaseSchema(BaseModel):
    name: str
    password: str

    class Config:
        orm_mode = True


class ResetPasswordBaseSchema(BaseModel):
    user_id: str
    password: str
    new_password: str

    class Config:
        orm_mode = True


class RegisterResponse(BaseModel):
    user_id: int
    name: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    user_id: int
    name: str
    authority_id: int

    class Config:
        orm_mode = True
