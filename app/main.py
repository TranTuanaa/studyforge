from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.base import engine, Base

# Import routers
from app.routers.subject import router as subject_router
from app.routers.fixed_time_slot import router as fixed_slot_router
from app.routers.class_schedule import router as class_schedule_router
from app.routers.optimization import router as optimization_router

app = FastAPI(
    title="StudyForge API",
    description="Smart Study Scheduler Backend - Tối ưu lịch học bằng Linear Programming",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected & tables created!")

@app.get("/")
async def root():
    return {"message": "StudyForge Backend is running! 🚀"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected"}

# Include routers
app.include_router(subject_router)
app.include_router(fixed_slot_router)
app.include_router(class_schedule_router)
app.include_router(optimization_router)