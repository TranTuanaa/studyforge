from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud.fixed_time_slot import create_fixed_slot, get_fixed_slots
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(
    prefix="/fixed-time-slots",
    tags=["Fixed Time Slots"]
)

ALLOWED_FRAMES = [(7, 11), (13, 17), (19, 22)]

def is_in_allowed_frame(start_time: str, end_time: str) -> bool:
    try:
        s = int(str(start_time)[:2])
        e = int(str(end_time)[:2])
        for start_frame, end_frame in ALLOWED_FRAMES:
            if start_frame <= s and e <= end_frame:
                return True
        return False
    except:
        return False

@router.post("/", response_model=FixedTimeSlotResponse)
def create_fixed_time_slot(slot: FixedTimeSlotCreate, db: Session = Depends(get_db)):
    if not is_in_allowed_frame(slot.start_time, slot.end_time):
        raise HTTPException(
            status_code=400,
            detail="Fixed time slot phải nằm trong 3 khung giờ: 7-11, 13-17, 19-22"
        )
    return create_fixed_slot(db=db, slot=slot)

@router.get("/", response_model=List[FixedTimeSlotResponse])
def read_fixed_time_slots(db: Session = Depends(get_db)):
    return get_fixed_slots(db)