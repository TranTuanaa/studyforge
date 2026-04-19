from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.import_service import import_csv

router = APIRouter(prefix="/import", tags=["Import All Data"])


@router.post("/all/")
async def import_all_data_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await import_csv(file=file, db=db)
