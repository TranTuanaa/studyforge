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
async def import_subjects_from_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Import danh sách môn học từ file CSV (không dùng pandas)"""
    
    if not file.filename.lower().endswith('.csv'):
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ file CSV (.csv)")

    try:
        content = await file.read()
        stream = io.StringIO(content.decode("utf-8"))
        reader = csv.DictReader(stream)

        created = 0
        errors = 0

        for row in reader:
            try:
                subject = SubjectCreate(
                    name=str(row.get("name") or row.get("Tên môn") or row.get("Tên")).strip(),
                    credits=int(row.get("credits") or row.get("Tín chỉ") or 3),
                    priority=int(row.get("priority") or row.get("Độ ưu tiên") or row.get("Ưu tiên") or 5),
                    difficulty=int(row.get("difficulty") or row.get("Độ khó") or 5)
                )
                create_subject(db=db, subject=subject)
                created += 1
            except Exception as e:
                print(f"Lỗi import dòng '{row}': {e}")
                errors += 1
                continue

        return {
            "message": f"Import hoàn tất. Thành công: {created} môn | Lỗi: {errors} dòng",
            "total_processed": created + errors
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc file CSV: {str(e)}")