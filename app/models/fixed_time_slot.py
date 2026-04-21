from sqlalchemy import Column, Integer, String, Time

from app.models.base import Base


class FixedTimeSlot(Base):
    __tablename__ = "fixed_time_slots"

    id = Column(Integer, primary_key=True, index=True)
    day_of_week = Column(Integer, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    activity = Column(String, nullable=False)
