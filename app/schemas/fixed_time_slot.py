from datetime import time

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FixedTimeSlotBase(BaseModel):
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    activity: str = Field(min_length=1, max_length=100)

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class FixedTimeSlotCreate(FixedTimeSlotBase):
    pass


class FixedTimeSlotResponse(FixedTimeSlotBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
