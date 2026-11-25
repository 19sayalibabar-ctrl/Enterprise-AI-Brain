"""Application entry point: FastAPI app, middleware, and router registration."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.auth import router as auth_router
from api.chat import router as chat_router
from api.documents import router as documents_router
from config.settings import get_settings
from database.db import init_db

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run startup logic. Creates database tables before serving requests."""
    init_db()
    yield


app = FastAPI(
    title="Enterprise AI Brain",
    description="Multi-agent knowledge assistant with RAG, memory, and planning.",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", tags=["system"])
def health_check() -> dict:
    """Simple liveness probe used by the frontend and for manual checks."""
    return {"status": "ok", "environment": settings.app_env}


app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(chat_router)
