from fastapi import APIRouter, Depends, status
from ..schemas.response_schema import ResponseData
from ..db.database import get_db
from sqlalchemy.orm import Session
from ..crud.car import read_car, soft_delete, add_car, all_cars
from ..utils.logger import setup_logger
from ..utils.exception import (
    NotFoundException,
)
from typing import List

from ..models.car import Car
from ..schemas.car import CarResponseSchema, CreateCarSchema

router = APIRouter()
logger = setup_logger(__name__)


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseData,
)
async def create_car(
    car_data: CreateCarSchema,
    db: Session = Depends(get_db),
):
    hash_car_data = car_data.dict()

    car: Car = Car(**hash_car_data)
    new_car = await add_car(car, db)

    return new_car.__dict__

@router.get(
    "/get-car/{car_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=CarResponseSchema,
)
async def get_car(car_id: int, db: Session = Depends(get_db)):
    car = read_car(car_id, db)

    if car is None:
        logger.info(f"Invalid car id {car_id}")
        raise NotFoundException(detail=f"Invalid car id")

    return car.__dict__

@router.get(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[CarResponseSchema],
)
async def get_cars(db: Session = Depends(get_db)):
    car = await all_cars(db)
    rs = [i.__dict__ for i in car]
    return rs

@router.post("/soft-delete/{car_id}", response_model=CarResponseSchema)
async def soft_delete_by_id(car_id: int, db: Session = Depends(get_db)):
    car = soft_delete(car_id, db)

    if car is None:
        logger.info(f"Invalid car with ID: {car_id}")
        raise NotFoundException(detail=f"Invalid car with ID: {car_id}")
    logger.info(f"Soft delete car with ID: {car_id}")
    return car.__dict__