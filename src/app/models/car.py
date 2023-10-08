import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


class Car(Base):
    __tablename__ = "cars"
    
    car_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    model = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)
    
    class Config:
        orm_mode = True
