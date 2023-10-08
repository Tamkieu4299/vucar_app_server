import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as
from sqlalchemy.orm import Session

from ..crud.user import add_user, search_user, search_user_id, update_password
from ..db.database import get_db
from ..models.user import User
from ..schemas.auth import (
    LoginBaseSchema,
    LoginResponse,
    RegisterBaseSchema,
    RegisterResponse,
    ResetPasswordBaseSchema,
)
from ..schemas.response_schema import ResponseData
from ..utils.exception import InvalidDestination, InvalidFileType, NotFoundException
from ..utils.handle_file import validate_file_type
from ..utils.hash import hash_password, verify_password
from ..utils.logger import setup_logger
from ..utils.response import convert_response

logger = setup_logger(__name__)

router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def register_user(
    user_data: RegisterBaseSchema,
    db: Session = Depends(get_db),
):
    hash_user_data = user_data.dict()
    hash_user_data["password"] = hash_password(hash_user_data["password"])

    user: User = User(**hash_user_data)
    new_user = await add_user(user, db)

    if new_user is None:
        logger.info(f"Phone number {user_data.phone} has been registered")
        raise InvalidDestination(detail=f"Phone number has been registered")
    response_data = parse_obj_as(RegisterResponse, new_user.__dict__)
    return convert_response(True, "Register Successfully", response_data)


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def login(
    login_data: LoginBaseSchema,
    db: Session = Depends(get_db),
):
    user = search_user(login_data.name, db)

    if user is None:
        logger.info(f"Invalid phone number")
        raise NotFoundException(detail=f"Invalid user name")

    valid_password = verify_password(login_data.password, user.password)

    if not valid_password:
        logger.info(f"Invalid password")
        raise InvalidDestination(detail=f"Invalid password")
    response_data = parse_obj_as(LoginResponse, user.__dict__)
    return convert_response(True, "Login Successfully", response_data)


@router.post(
    "/reset-password",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def reset_password(
    reset_pasword_data: ResetPasswordBaseSchema,
    db: Session = Depends(get_db),
):
    new_password = hash_password(reset_pasword_data.new_password)
    user = search_user_id(reset_pasword_data.user_id, db)

    if user is None:
        logger.info(f"Invalid user id {reset_pasword_data.user_id}")
        raise NotFoundException(detail=f"Invalid user id")

    valid_password = verify_password(reset_pasword_data.password, user.password)

    if not valid_password:
        logger.info(f"Invalid password")
        raise InvalidDestination(detail=f"Invalid password")
    new_user = update_password(reset_pasword_data.user_id, new_password, db)
    logger.info(
        f"Update old password {user.password} to new password {new_user.password}"
    )
    response_data = parse_obj_as(LoginResponse, user.__dict__)
    return convert_response(True, "Change password Successfully", response_data)
