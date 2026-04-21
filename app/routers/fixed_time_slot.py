from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.study_frames import has_study_frame_overlap
from app.crud.fixed_time_slot import (
    create_fixed_time_slot as create_fixed_time_slot_record,
    get_fixed_time_slots,
)
from app.database import get_db
from app.schemas.fixed_time_slot import FixedTimeSlotCreate, FixedTimeSlotResponse

router = APIRouter(prefix="/fixed-time-slots", tags=["Fixed Time Slots"])


@router.post("/", response_model=FixedTimeSlotResponse)
def create_fixed_time_slot_endpoint(slot: FixedTimeSlotCreate, db: Session = Depends(get_db)):
    if not has_study_frame_overlap(slot.start_time, slot.end_time):
        raise HTTPException(
            status_code=400,
            detail="Fixed time slot must overlap at least one study frame: 7-11, 13-17, or 19-22",
        )

    return create_fixed_time_slot_record(db=db, slot=slot)


@router.get("/", response_model=list[FixedTimeSlotResponse])
def read_fixed_time_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_fixed_time_slots(db, skip=skip, limit=limit)
