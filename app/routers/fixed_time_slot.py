from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.study_frames import is_within_study_frames
from app.crud.fixed_time_slot import create_fixed_slot, get_fixed_slots
from app.database import get_db
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(prefix="/fixed-time-slots", tags=["Fixed Time Slots"])


@router.post("/", response_model=FixedTimeSlotResponse)
def create_fixed_time_slot(slot: FixedTimeSlotCreate, db: Session = Depends(get_db)):
    if not is_within_study_frames(slot.start_time, slot.end_time):
        raise HTTPException(
            status_code=400,
            detail="Fixed time slot must stay inside 7-11, 13-17, or 19-22",
        )

    return create_fixed_slot(db=db, slot=slot)


@router.get("/", response_model=list[FixedTimeSlotResponse])
def read_fixed_time_slots(db: Session = Depends(get_db)):
    return get_fixed_slots(db)
