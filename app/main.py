from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.models.base import Base
from app.routers.class_schedule import router as class_schedule_router
from app.routers.export_schedule import router as export_router
from app.routers.fixed_time_slot import router as fixed_slot_router
from app.routers.import_all import router as import_all_router
from app.routers.optimization import router as optimization_router
from app.routers.subject import router as subject_router

app = FastAPI(
    title="StudyForge API",
    description="Smart Study Scheduler Backend",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "StudyForge Backend is running!"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


app.include_router(subject_router)
app.include_router(fixed_slot_router)
app.include_router(class_schedule_router)
app.include_router(optimization_router)
app.include_router(import_all_router)
app.include_router(export_router)
