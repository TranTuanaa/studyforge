from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.subject import create_subject, get_subjects
from app.schemas.subject import SubjectCreate, SubjectResponse

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post("/", response_model=SubjectResponse)
def create_new_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    return create_subject(db, subject)

@router.get("/", response_model=list[SubjectResponse])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_subjects(db, skip=skip, limit=limit)