from datetime import time
import csv
import io

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.class_schedule import ClassSchedule
from app.models.fixed_time_slot import FixedTimeSlot
from app.models.subject import Subject

ALLOWED_FRAMES = [(7, 11), (13, 17), (19, 22)]
VALID_TYPES = {"subject", "class_schedule", "fixed_time"}


def read_rows(content: bytes) -> list[dict]:
    try:
        reader = csv.DictReader(io.StringIO(content.decode("utf-8-sig")))
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc

    rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader]
    if not reader.fieldnames or not rows:
        raise HTTPException(status_code=400, detail="CSV must include a header and at least one data row")
    return rows


def required(row: dict, field: str) -> str:
    value = row.get(field, "")
    if not value:
        raise ValueError(f"Missing required field: {field}")
    return value


def parse_int(row: dict, field: str, default: int | None = None) -> int:
    value = row.get(field, "")
    if value == "":
        if default is not None:
            return default
        raise ValueError(f"Missing required field: {field}")
    return int(value)


def parse_day(row: dict) -> int:
    day = parse_int(row, "day_of_week")
    if day not in range(7):
        raise ValueError("day_of_week must be from 0 to 6")
    return day


def parse_time(row: dict, field: str) -> time:
    parts = required(row, field).split(":")
    if len(parts) < 2:
        raise ValueError(f"{field} must use HH:MM format")
    return time(hour=int(parts[0]), minute=int(parts[1]))


def parse_interval(row: dict, fixed_time: bool = False) -> tuple[time, time]:
    start = parse_time(row, "start_time")
    end = parse_time(row, "end_time")
    if (end.hour, end.minute) <= (start.hour, start.minute):
        raise ValueError("end_time must be after start_time")

    start_hour = start.hour + start.minute / 60
    end_hour = end.hour + end.minute / 60
    if fixed_time and not any(a <= start_hour and end_hour <= b for a, b in ALLOWED_FRAMES):
        raise ValueError("fixed_time must stay inside 7-11, 13-17, or 19-22")

    return start, end


def find_subject_id(row: dict, db: Session, subjects: dict[str, Subject]) -> int:
    if row.get("subject_id"):
        subject = db.get(Subject, int(row["subject_id"]))
        if subject:
            return subject.id
        raise ValueError(f"subject_id {row['subject_id']} does not exist")

    subject_name = row.get("subject_name") or row.get("name")
    if subject_name in subjects:
        return subjects[subject_name].id
    raise ValueError("class_schedule requires an existing subject_id or subject_name")


async def import_csv(file: UploadFile, db: Session) -> dict:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    rows = read_rows(await file.read())
    subjects = {subject.name: subject for subject in db.query(Subject).all()}
    added = {"subjects": 0, "class_schedules": 0, "fixed_slots": 0}

    try:
        for row_number, row in enumerate(rows, start=2):
            kind = row.get("type", "")
            if kind not in VALID_TYPES:
                raise ValueError("type must be subject, class_schedule, or fixed_time")

            if kind == "subject":
                name = required(row, "name")
                if name in subjects:
                    continue

                subject = Subject(
                    name=name,
                    credits=parse_int(row, "credits", 3),
                    priority=parse_int(row, "priority", 5),
                    difficulty=parse_int(row, "difficulty", 5),
                )
                db.add(subject)
                db.flush()
                subjects[name] = subject
                added["subjects"] += 1

            elif kind == "class_schedule":
                start, end = parse_interval(row)
                db.add(
                    ClassSchedule(
                        subject_id=find_subject_id(row, db, subjects),
                        day_of_week=parse_day(row),
                        start_time=start,
                        end_time=end,
                        room=row.get("room") or None,
                    )
                )
                added["class_schedules"] += 1

            else:
                start, end = parse_interval(row, fixed_time=True)
                db.add(
                    FixedTimeSlot(
                        day_of_week=parse_day(row),
                        start_time=start,
                        end_time=end,
                        activity=required(row, "activity"),
                    )
                )
                added["fixed_slots"] += 1

        db.commit()
    except (TypeError, ValueError) as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Row {row_number}: {exc}") from exc
    except SQLAlchemyError as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database import failed: {exc}") from exc

    return {"message": "Import completed", "details": added}
