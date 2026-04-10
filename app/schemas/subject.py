from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SubjectBase(BaseModel):
    name: str
    credits: int
    difficulty: int = 5
    priority: int = 5

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)