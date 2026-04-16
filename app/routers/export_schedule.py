from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import pandas as pd
import tempfile

from app.database import get_db
from app.routers.optimization import optimize_schedule

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)

@router.post("/schedule/")
def export_schedule_to_excel(db: Session = Depends(get_db)):
    result = optimize_schedule(db=db)

    data = []
    for subj in result["schedule"]:
        row = {"Môn học": subj["subject"], "Tổng giờ": subj["total_hours"]}
        for i, hours in enumerate(subj["daily_hours"]):
            row[f"Thứ {i+2}"] = hours
        data.append(row)

    df = pd.DataFrame(data)

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        df.to_excel(tmp.name, index=False)
        tmp_path = tmp.name

    return FileResponse(
        tmp_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="ThoiKhoaBieu_StudyForge.xlsx"
    )