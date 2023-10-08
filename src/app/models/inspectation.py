import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


class Inspectation(Base):
    __tablename__ = "inspectations"
    
    inspectation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    car_id = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False)

    class Config:
        orm_mode = True
