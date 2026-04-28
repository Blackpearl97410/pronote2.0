from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.auth.router import router as auth_router
from backend.routers.grades import router as grades_router
from backend.routers.absences import router as absences_router
from backend.routers.messages import router as messages_router
from backend.routers.homework import router as homework_router
from backend.routers.schedule import router as schedule_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API de gestion scolaire — Pronote 2.0",
)

# CORS — autoriser Streamlit en dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(grades_router)
app.include_router(absences_router)
app.include_router(messages_router)
app.include_router(homework_router)
app.include_router(schedule_router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "healthy"}
