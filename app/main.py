from fastapi import FastAPI
from app.database import engine

app = FastAPI(
    title="Excel Data Import & Validation System",
    version="1.0.0",
    description="System for customer management and large-scale Excel data imports.",
)


@app.get("/")
def health_check():
    return {
        "message": "Excel Data Import & Validation System is running"
    }


@app.get("/health")
def db_connection_check():
    try:
        with engine.connect():
            return {
                "status": "healthy",
                "database": "connected",
            }
    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }