from pydantic import BaseModel
from typing import Optional
from datetime import time

class ClassScheduleBase(BaseModel):
    subject_id: int
    day_of_week: int                    # 0 = Thứ 2, ..., 6 = Chủ Nhật
    start_time: time
    end_time: time
    room: Optional[str] = None

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleResponse(ClassScheduleBase):
    id: int

    class Config:
        from_attributes = True