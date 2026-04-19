from datetime import time
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.fixed_time_slot import create_fixed_slot, get_fixed_slots
from app.database import get_db
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(prefix="/fixed-time-slots", tags=["Fixed Time Slots"])

ALLOWED_FRAMES = [(7, 11), (13, 17), (19, 22)]


def time_to_hour(value: time) -> float:
    return value.hour + value.minute / 60


def is_in_allowed_frame(start_time: time, end_time: time) -> bool:
    start_hour = time_to_hour(start_time)
    end_hour = time_to_hour(end_time)
    return any(start <= start_hour and end_hour <= end for start, end in ALLOWED_FRAMES)


@router.post("/", response_model=FixedTimeSlotResponse)
def create_fixed_time_slot(slot: FixedTimeSlotCreate, db: Session = Depends(get_db)):
    if slot.end_time <= slot.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")

    if not is_in_allowed_frame(slot.start_time, slot.end_time):
        raise HTTPException(
            status_code=400,
            detail="Fixed time slot must stay inside 7-11, 13-17, or 19-22",
        )

    return create_fixed_slot(db=db, slot=slot)


@router.get("/", response_model=List[FixedTimeSlotResponse])
def read_fixed_time_slots(db: Session = Depends(get_db)):
    return get_fixed_slots(db)
