from datetime import time

from pydantic import BaseModel, ConfigDict


class FixedTimeSlotBase(BaseModel):
    day_of_week: int
    start_time: time
    end_time: time
    activity: str


class FixedTimeSlotCreate(FixedTimeSlotBase):
    pass


class FixedTimeSlotResponse(FixedTimeSlotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
