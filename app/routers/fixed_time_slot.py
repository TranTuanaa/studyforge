from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import time
from typing import List
from app.database import get_db
from app.crud.fixed_time_slot import create_fixed_slot, get_fixed_slots
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(
    prefix="/fixed-slots",
    tags=["Fixed Time Slots"]
)

ALLOWED_FRAMES = [(7, 11), (13, 17), (19, 22)]

def is_in_allowed_frame(start_time, end_time) -> bool:
    """Kiểm tra slot có nằm trong 3 khung giờ cho phép không (hỗ trợ cả string và time object)"""
    try:
        # Chuyển sang số giờ float
        if isinstance(start_time, time):
            s = start_time.hour + start_time.minute / 60.0
        else:
            s = float(str(start_time)[:2]) + float(str(start_time)[3:5]) / 60.0

        if isinstance(end_time, time):
            e = end_time.hour + end_time.minute / 60.0
        else:
            e = float(str(end_time)[:2]) + float(str(end_time)[3:5]) / 60.0

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