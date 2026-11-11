from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.routers.auth import router as auth_router
from app.config import get_settings
from app.database import check_database, get_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    get_settings()  # Validate configuration before accepting requests.
    yield
    get_engine().dispose()


app = FastAPI(title="FieldFlow API", version="0.1.0", lifespan=lifespan)
app.include_router(auth_router)

@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    """Liveness: the API is running, regardless of database availability."""
    return {"status": "ok"}


@app.get("/health/db", tags=["health"])
def database_health() -> dict[str, str]:
    """Readiness: verify a real database query without creating any tables."""
    try:
        check_database()
    except SQLAlchemyError:
        raise HTTPException(status_code=503, detail="Database unavailable") from None
    return {"status": "ok", "database": "ok"}
