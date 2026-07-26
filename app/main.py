from fastapi import FastAPI

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