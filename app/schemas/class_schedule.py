from datetime import time
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClassScheduleBase(BaseModel):
    subject_id: int
    day_of_week: int
    start_time: time
    end_time: time
    room: Optional[str] = None


class ClassScheduleCreate(ClassScheduleBase):
    pass


class ClassScheduleResponse(ClassScheduleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
