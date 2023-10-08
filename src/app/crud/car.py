from sqlalchemy.orm import Session
from typing import List

from ..models.car import Car

async def add_car(car: Car, db: Session) -> Car:
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


def read_car(car_id: int, db: Session) -> Car:
    car = (
        db.query(Car)
        .filter(Car.car_id == car_id and Car.is_deleted == False)
        .first()
    )
    return car


def soft_delete(car_id: str, db: Session) -> Car:
    car = (
        db.query(Car)
        .where(Car.car_id == car_id and Car.is_deleted == False)
        .first()
    )
    if car:
        car.is_deleted = True
        db.commit()
        db.refresh(car)
        return car
    return None


def search_car(name: str, db: Session) -> Car:
    car = (
        db.query(Car)
        .filter(Car.name == name and Car.is_deleted == False)
        .first()
    )
    return car


async def all_cars(db: Session) -> List[Car]:
    db_cars = db.query(Car).filter(Car.is_deleted == False).all()
    return db_cars
