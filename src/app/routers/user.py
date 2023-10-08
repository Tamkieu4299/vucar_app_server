import os
import uuid
from typing import List

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.staticfiles import StaticFiles
from pydantic import parse_obj_as
from sqlalchemy.orm import Session
from ..crud.user import (
    add_user,
    search_user,
    search_user_id,
    search_users_by_name,
    update_password,
    all_users,
    soft_delete,
    update_playlist,
)
from ..db.database import get_db
from ..models.user import User
from ..schemas.response_schema import ResponseData
from ..schemas.user import UserResponseSchema, UserUpdateSchema
from ..utils.exception import (
    InvalidDestination,
    InvalidFileType,
    NotFoundException,
)
from ..utils.handle_file import validate_file_type
from ..utils.hash import hash_password, verify_password
from ..utils.logger import setup_logger
from ..utils.response import convert_response

logger = setup_logger(__name__)

router = APIRouter()


@router.get(
    "/get-user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def get_user(user_id: str, db: Session = Depends(get_db)):
    user = search_user_id(user_id, db)

    if user is None:
        logger.info(f"Invalid user id {user_id}")
        raise NotFoundException(detail=f"Invalid user id")

    response_data = parse_obj_as(UserResponseSchema, user.__dict__)
    return convert_response(True, "", response_data)


@router.get("/search/", response_model=List[UserResponseSchema])
async def get_users(db: Session = Depends(get_db)):
    users = await all_users(db)
    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list


@router.post("/soft-delete/{user_id}", response_model=UserResponseSchema)
async def soft_delete_by_id(user_id: str, db: Session = Depends(get_db)):
    user = soft_delete(user_id, db)

    if user is None:
        logger.info(f"Invalid user with ID: {user_id}")
        raise NotFoundException(detail=f"Invalid user with ID: {user_id}")
    logger.info(f"Soft delete user with ID: {user_id}")
    return user.__dict__


@router.get("/search/{name}", response_model=List[UserResponseSchema])
async def search_users(name: str, db: Session = Depends(get_db)):
    users = await search_users_by_name(name, db)
    users_dict_list = [i.__dict__ for i in users]
    logger.info(f"Number of users: {len(users)}")
    return users_dict_list
