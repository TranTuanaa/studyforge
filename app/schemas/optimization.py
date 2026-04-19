from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SubjectInput(BaseModel):
    name: str
    priority: int = 5
    hours_wanted: float
    deadline: Optional[datetime] = None


class FixedSlotInput(BaseModel):
    day_of_week: int
    activity: str


class ClassScheduleInput(BaseModel):
    subject_id: int
    day_of_week: int
    start_time: str
    end_time: str
    room: Optional[str] = None


class OptimizeRequest(BaseModel):
    subjects: List[SubjectInput]
    fixed_slots: List[FixedSlotInput] = Field(default_factory=list)
    class_schedules: List[ClassScheduleInput] = Field(default_factory=list)
    days: int = 7


class OptimizeResponse(BaseModel):
    status: str
    objective_value: Optional[float]
    schedule: List[dict]
    message: str
