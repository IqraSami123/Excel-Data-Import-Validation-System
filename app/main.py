from fastapi import FastAPI
from app.database import engine
from app.api.customers import router as customer_router

app = FastAPI(
    title="Excel Data Import & Validation System",
    version="1.0.0",
    description="System for customer management and large-scale Excel data imports.",
)

app.include_router(customer_router)

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