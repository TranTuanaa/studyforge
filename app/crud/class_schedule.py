from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.class_schedule import ClassSchedule
from app.models.subject import Subject
from app.schemas.class_schedule import ClassScheduleCreate


def create_class_schedule(db: Session, schedule: ClassScheduleCreate):
    if not db.get(Subject, schedule.subject_id):
        raise HTTPException(status_code=400, detail=f"subject_id {schedule.subject_id} does not exist")

    db_schedule = ClassSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule


def get_class_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClassSchedule).offset(skip).limit(limit).all()
