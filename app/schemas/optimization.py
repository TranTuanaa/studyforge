from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubjectInput(BaseModel):
    name: str
    priority: int = 5
    hours_wanted: float
    deadline: Optional[datetime] = None

class FixedSlotInput(BaseModel):
    day_of_week: int
    activity: str

# Mới thêm: Lịch học trên trường
class ClassScheduleInput(BaseModel):
    subject_id: int
    day_of_week: int
    start_time: str          # ví dụ: "07:30"
    end_time: str            # ví dụ: "09:00"
    room: Optional[str] = None

class OptimizeRequest(BaseModel):
    subjects: List[SubjectInput]
    fixed_slots: List[FixedSlotInput] = []
    class_schedules: List[ClassScheduleInput] = []   # ← thêm cái này
    days: int = 7

class OptimizeResponse(BaseModel):
    status: str
    objective_value: Optional[float]
    schedule: List[dict]
    message: str