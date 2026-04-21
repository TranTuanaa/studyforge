from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.schemas.subject import SubjectCreate


def create_subject(db: Session, subject: SubjectCreate):
    existing_subject = db.query(Subject).filter(Subject.name == subject.name).first()
    if existing_subject:
        raise HTTPException(status_code=400, detail="Subject with this name already exists")

    db_subject = Subject(**subject.model_dump())
    db.add(db_subject)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail="Subject with this name already exists") from exc
    db.refresh(db_subject)
    return db_subject


def get_subjects(db: Session, skip: int = 0, limit: int | None = 100):
    query = db.query(Subject).offset(skip)
    if limit is not None:
        query = query.limit(limit)
    return query.all()
