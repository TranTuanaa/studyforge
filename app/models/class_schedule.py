from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.sql import func

from app.models.base import Base


class ClassSchedule(Base):
    __tablename__ = "class_schedules"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
