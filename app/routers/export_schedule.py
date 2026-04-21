import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers.optimization import build_optimized_schedule

router = APIRouter(prefix="/export", tags=["Export"])


@router.post("/schedule/")
def export_schedule_to_csv(db: Session = Depends(get_db)):
    result = build_optimized_schedule(db)

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Subject", "Total Hours", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

    for item in result["schedule"]:
        daily_hours = item["daily_hours"]
        writer.writerow(
            [
                item["subject"],
                item["total_hours"],
                daily_hours[0],
                daily_hours[1],
                daily_hours[2],
                daily_hours[3],
                daily_hours[4],
                daily_hours[5],
                daily_hours[6] if len(daily_hours) > 6 else 0,
            ]
        )

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue().encode("utf-8-sig")]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=studyforge_schedule.csv"},
    )
