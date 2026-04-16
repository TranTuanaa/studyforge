from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.subject import get_subjects
from app.crud.class_schedule import get_class_schedules
from app.crud.fixed_time_slot import get_fixed_slots
from app.services.optimization_service import OptimizationService

router = APIRouter(
    prefix="/optimize",
    tags=["Optimization"]
)

service = OptimizationService()

@router.post("/")
def optimize_schedule(db: Session = Depends(get_db)):
    """Tối ưu lịch tự học theo priority + thời gian rảnh thực tế"""
    try:
        # Lấy dữ liệu từ DB
        subjects = get_subjects(db)
        class_schedules = get_class_schedules(db)
        fixed_slots = get_fixed_slots(db)

        # Chuyển sang dict để service dùng
        subjects_list = [s.__dict__ for s in subjects]
        class_list = [cs.__dict__ for cs in class_schedules]
        fixed_list = [fs.__dict__ for fs in fixed_slots]

        # Gọi service
        result = service.optimize_schedule(
            subjects=subjects_list,
            class_schedules=class_list,
            fixed_slots=fixed_list,
            days=7
        )

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi tối ưu: {str(e)}")