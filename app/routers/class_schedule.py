from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.class_schedule import create_class_schedule, get_class_schedules
from app.schemas.class_schedule import ClassScheduleCreate, ClassScheduleResponse

router = APIRouter(prefix="/class-schedules", tags=["Class Schedules"])

@router.post("/", response_model=ClassScheduleResponse)
def create_new_class_schedule(schedule: ClassScheduleCreate, db: Session = Depends(get_db)):
    return create_class_schedule(db, schedule)

@router.get("/", response_model=list[ClassScheduleResponse])
def read_class_schedules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_class_schedules(db, skip=skip, limit=limit)