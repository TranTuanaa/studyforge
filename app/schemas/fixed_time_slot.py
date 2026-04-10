from pydantic import BaseModel
from typing import Optional
from datetime import time

class FixedTimeSlotBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    activity: str

class FixedTimeSlotCreate(FixedTimeSlotBase):
    pass

class FixedTimeSlotResponse(FixedTimeSlotBase):
    id: int

    class Config:
        from_attributes = True