from datetime import time

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ClassScheduleBase(BaseModel):
    subject_id: int = Field(gt=0)
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    room: str | None = None

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ClassScheduleCreate(ClassScheduleBase):
    pass


class ClassScheduleResponse(ClassScheduleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
