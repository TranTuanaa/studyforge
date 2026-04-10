from sqlalchemy.orm import Session
from app.models.class_schedule import ClassSchedule
from app.schemas.class_schedule import ClassScheduleCreate

def create_class_schedule(db: Session, schedule: ClassScheduleCreate):
    db_schedule = ClassSchedule(**schedule.model_dump())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def get_class_schedules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ClassSchedule).offset(skip).limit(limit).all()