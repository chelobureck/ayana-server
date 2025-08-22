import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import Base, engine
from .routers import health, auth, lesson, project

app = FastAPI(title="AI Tutor MVP", debug=settings.APP_DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.APP_CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(lesson.router, prefix="/api/v1")
app.include_router(project.router, prefix="/api/v1")

# Run: uvicorn app.main:app --host 0.0.0.0 --port 8000 