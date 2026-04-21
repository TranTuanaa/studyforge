from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.models.base import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    credits = Column(Integer, nullable=False)
    difficulty = Column(Integer, default=5)
    priority = Column(Integer, default=5)
    created_at = Column(DateTime, server_default=func.now())
