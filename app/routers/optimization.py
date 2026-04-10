from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.optimization_service import OptimizationService
from app.crud.subject import get_subjects
from app.crud.fixed_time_slot import get_fixed_slots
from app.crud.class_schedule import get_class_schedules

router = APIRouter(
    prefix="/optimize",
    tags=["Optimization"]
)

@router.post("/")
async def optimize_schedule(db: Session = Depends(get_db)):
    """Tối ưu lịch học - đã tính thời gian rảnh thực tế"""
    service = OptimizationService()
    
    subjects = get_subjects(db, limit=50)
    fixed_slots = get_fixed_slots(db, limit=50)
    class_schedules = get_class_schedules(db, limit=50)
    
    subjects_list = [{
        "name": s.name,
        "priority": s.priority
    } for s in subjects]
    
    result = service.optimize_schedule(
        subjects=subjects_list,
        class_schedules=[{"start_time": c.start_time, "end_time": c.end_time} for c in class_schedules],
        fixed_slots=[{"start_time": f.start_time, "end_time": f.end_time} for f in fixed_slots],
        days=7
    )
    return result