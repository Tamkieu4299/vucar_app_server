import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String, JSON
from sqlalchemy_json import MutableJson, NestedMutableJson
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ..db.database import Base
from sqlalchemy.ext.mutable import MutableDict

class Inspectation(Base):
    __tablename__ = "inspectations"

    inspectation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    car_id = Column(Integer, nullable=False)
    stats = Column(NestedMutableJson, nullable=True)
    is_deleted = Column(Boolean, default=False)

    class Config:
        orm_mode = True
