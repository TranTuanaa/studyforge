# StudyForge Backend

StudyForge is a FastAPI backend for importing study data, storing class schedules and fixed time slots, then generating a weekly self-study allocation based on subject priority.

## Features

- Basic CRUD APIs for subjects, fixed time slots, and class schedules
- CSV import for full study data: subjects, class schedules, and fixed time slots
- Weekly optimization based on real free time for each day and subject priority
- CSV export for the generated study schedule
- Swagger UI for quick testing

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic v2
- SQLite
- Uvicorn

## Run Locally

Project target Python version: `3.12.8` from `.python-version`.

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Optional environment file:

```powershell
Copy-Item .env.example .env
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

## Live Demo

- API root: https://studyforge-cn7l.onrender.com
- Swagger UI: https://studyforge-cn7l.onrender.com/docs
- Sample CSV: `sample_import_all.csv`

## Main APIs

- `POST /import/all/` - import full CSV data
- `POST /optimize/` - generate weekly study-hour allocation by day
- `POST /export/schedule/` - export schedule as CSV
- `GET/POST /subjects/`
- `GET/POST /fixed-time-slots/`
- `GET/POST /class-schedules/`

## CSV Import Format

Use `sample_import_all.csv` as a ready-to-test file in Swagger.

```csv
type,name,credits,priority,difficulty,subject_name,subject_id,day_of_week,start_time,end_time,activity,room
subject,Math,3,8,6,,,,,,,
subject,Physics,4,7,8,,,,,,,
class_schedule,,,,,Math,,0,07:00,09:00,,A101
class_schedule,,,,,Physics,,2,13:00,15:00,,B202
fixed_time,,,,,,,1,19:00,20:00,Gym,
fixed_time,,,,,,,4,13:00,14:00,Part-time job,
```

`day_of_week` uses `0 = Monday` through `6 = Sunday`.

## Code Structure

- `app/routers/` contains API endpoints
- `app/schemas/` contains Pydantic request/response models
- `app/models/` contains SQLAlchemy models
- `app/crud/` contains database operations
- `app/services/` contains import and optimization logic
- Database tables are created automatically on startup
- CSV import uses rollback if any row fails
- Optimization returns daily study hours per subject, not exact calendar time blocks
