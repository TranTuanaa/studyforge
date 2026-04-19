from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.class_schedule import get_class_schedules
from app.crud.fixed_time_slot import get_fixed_slots
from app.crud.subject import get_subjects
from app.database import get_db
from app.services.optimization_service import OptimizationService

router = APIRouter(prefix="/optimize", tags=["Optimization"])
service = OptimizationService()


def subject_to_dict(subject) -> dict:
    return {
        "name": subject.name,
        "credits": subject.credits,
        "difficulty": subject.difficulty,
        "priority": subject.priority,
    }


def time_block_to_dict(item) -> dict:
    return {
        "day_of_week": item.day_of_week,
        "start_time": item.start_time,
        "end_time": item.end_time,
    }


@router.post("/")
def optimize_schedule(db: Session = Depends(get_db)):
    try:
        return service.optimize_schedule(
            subjects=[subject_to_dict(subject) for subject in get_subjects(db)],
            class_schedules=[time_block_to_dict(item) for item in get_class_schedules(db)],
            fixed_slots=[time_block_to_dict(item) for item in get_fixed_slots(db)],
            days=7,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Optimization failed: {exc}") from exc
