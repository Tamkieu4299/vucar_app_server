import uuid

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..db.database import Base


class Authority(Base):
    __tablename__ = "authorities"
    
    authority_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # Permissions
    inspect = Column(Boolean, default=False)
    view = Column(Boolean, default=False)
    user_edit =  Column(Boolean, default=False)

    is_deleted = Column(Boolean, default=False)

    class Config:
        orm_mode = True
