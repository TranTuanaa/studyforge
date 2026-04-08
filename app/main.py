from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.base import engine, Base

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

# Tạo bảng khi khởi động (chỉ dùng trong dev)
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("✅ Database connected & tables created!")

@app.get("/")
async def root():
    return {
        "message": "StudyForge Backend is running! 🚀",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected"}