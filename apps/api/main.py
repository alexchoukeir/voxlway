from fastapi import FastAPI, status
from routers import search

app = FastAPI()

app.include_router(search.router, prefix="/api/v1")

@app.get("/health")
def read_health():
    """
    Verify that the API is running.
    """
    return {"status": "ok"}
