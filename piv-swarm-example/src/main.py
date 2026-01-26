"""Todo API - Main Application."""
from fastapi import FastAPI

app = FastAPI(
    title="Todo API",
    description="Simple Todo API for PIV-Swarm testing",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
