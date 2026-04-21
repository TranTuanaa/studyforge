from sqlalchemy.orm import Session

from app.models.fixed_time_slot import FixedTimeSlot
from app.schemas.fixed_time_slot import FixedTimeSlotCreate


def create_fixed_time_slot(db: Session, slot: FixedTimeSlotCreate):
    db_slot = FixedTimeSlot(**slot.model_dump())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot


def get_fixed_time_slots(db: Session, skip: int = 0, limit: int | None = 100):
    query = db.query(FixedTimeSlot).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()
