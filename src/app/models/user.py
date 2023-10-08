import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    authority_id = Column(Integer, default=2)
    is_deleted = Column(Boolean, default=False)

    class Config:
        orm_mode = True
