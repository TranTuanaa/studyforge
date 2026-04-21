from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SubjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    credits: int = Field(gt=0)
    difficulty: int = Field(ge=1, le=10, default=5)
    priority: int = Field(ge=1, le=10, default=5)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("name must not be empty")
        return cleaned


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
