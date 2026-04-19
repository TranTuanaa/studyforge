from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from app.database import get_db, engine
from app.models.base import Base

# Import routers
from app.routers.subject import router as subject_router
from app.routers.fixed_time_slot import router as fixed_slot_router
from app.routers.class_schedule import router as class_schedule_router
from app.routers.optimization import router as optimization_router
from app.routers.import_all import router as import_all_router
from app.routers.export_schedule import router as export_router

app = FastAPI(
    title="StudyForge API",
    description="Smart Study Scheduler Backend",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    print("Database connected & tables created!")

@app.get("/")
async def root():
    return {"message": "StudyForge Backend is running!"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    return {"status": "ok", "database": "connected"}

# Include routers
app.include_router(subject_router)
app.include_router(fixed_slot_router)
app.include_router(class_schedule_router)
app.include_router(optimization_router)
app.include_router(import_all_router)
app.include_router(export_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    method_order = ["post", "get", "put", "patch", "delete", "options", "head"]
    for path_methods in schema["paths"].values():
        ordered_methods = {
            method: path_methods[method]
            for method in method_order
            if method in path_methods
        }
        path_methods.clear()
        path_methods.update(ordered_methods)

    app.openapi_schema = schema
    return app.openapi_schema


app.openapi = custom_openapi

print("All routers loaded successfully!")
