from sqlalchemy.orm import Session
from app.models.fixed_time_slot import FixedTimeSlot
from app.schemas.fixed_time_slot import FixedTimeSlotCreate

def create_fixed_slot(db: Session, slot: FixedTimeSlotCreate):
    db_slot = FixedTimeSlot(**slot.model_dump())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

def get_fixed_slots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FixedTimeSlot).offset(skip).limit(limit).all()