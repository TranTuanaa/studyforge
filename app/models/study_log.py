from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from app.models.base import Base

class StudyLog(Base):
    __tablename__ = "study_logs"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    date = Column(DateTime, default=func.now())
    hours_spent = Column(Float, nullable=False)
    note = Column(String, nullable=True)