from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StudyForge API",
    description="Smart Study Scheduler Backend - Tối ưu lịch học bằng Linear Programming",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS cho phép test từ browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "StudyForge Backend is running! 🚀",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}