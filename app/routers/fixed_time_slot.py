from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.fixed_time_slot import create_fixed_slot, get_fixed_slots
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(
    prefix="/fixed-slots",
    tags=["Fixed Time Slots"]
)

ALLOWED_FRAMES = [(7, 11), (13, 17), (19, 22)]

def is_in_allowed_frame(start_time: str, end_time: str) -> bool:
    """Kiểm tra slot có nằm trong 3 khung giờ cho phép không"""
    try:
        s = float(start_time[:2]) + float(start_time[3:]) / 60
        e = float(end_time[:2]) + float(end_time[3:]) / 60
        for frame_start, frame_end in ALLOWED_FRAMES:
            if max(s, frame_start) < min(e, frame_end):
                return True
        return False
    except:
        return False

@router.post("/", response_model=FixedTimeSlotResponse)
def create_fixed_time_slot(
    slot: FixedTimeSlotCreate,
    db: Session = Depends(get_db)
):
    """Tạo fixed slot - CHỈ cho phép trong 3 khung giờ 7-11, 13-17, 19-22"""
    if not is_in_allowed_frame(slot.start_time, slot.end_time):
        raise HTTPException(
            status_code=400,
            detail="Fixed slot chỉ được tạo trong 3 khung giờ: 7-11, 13-17, 19-22"
        )
    
    return create_fixed_slot(db=db, slot=slot)

@router.get("/")
def read_fixed_slots(db: Session = Depends(get_db)):
    return get_fixed_slots(db)

# Các endpoint khác (nếu có PUT, DELETE...) giữ nguyên hoặc thêm sau