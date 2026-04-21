from typing import Literal

from pydantic import BaseModel, Field


class StudyPlanItem(BaseModel):
    subject: str = Field(min_length=1, max_length=100)
    allocated_hours: float = Field(ge=0)
    daily_hours: list[float]


class StudyPlanResponse(BaseModel):
    status: Literal["generated"]
    total_free_hours: float = Field(ge=0)
    study_plan: list[StudyPlanItem]
    message: str
