from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import csv
import io

from app.database import get_db
from app.crud.subject import create_subject
from app.schemas.subject import SubjectCreate

router = APIRouter(
    prefix="/import",
    tags=["Import Data"]
)

@router.post("/subjects/")
async def import_subjects_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file .csv")

    content = await file.read()
    csv_file = io.StringIO(content.decode("utf-8"))
    reader = csv.DictReader(csv_file)

    added = 0
    for row in reader:
        try:
            subject = SubjectCreate(
                name=row.get("name") or row.get("Tên môn") or row.get("subject"),
                credits=int(row.get("credits") or row.get("Tín chỉ") or 3),
                priority=int(row.get("priority") or row.get("Độ ưu tiên") or 5),
                difficulty=int(row.get("difficulty") or row.get("Độ khó") or 5)
            )
            create_subject(db=db, subject=subject)
            added += 1
        except:
            continue

    return {"message": f"✅ Import thành công {added} môn học từ file CSV"}