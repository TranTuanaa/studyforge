from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.study_plan import StudyPlanResponse
from app.services.study_plan_service import build_study_plan

router = APIRouter(prefix="/optimize", tags=["Study Plan"])


@router.post("/", response_model=StudyPlanResponse)
def generate_study_plan(db: Session = Depends(get_db)):
    return build_study_plan(db)
