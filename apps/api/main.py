import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter

ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

app = FastAPI(title="API")

app.include_router(search.router, prefix="/api/v1")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

if ENVIRONMENT == "development":
    cors_origins = ["http://localhost:3000"]
else:
    cors_origins = ["https://voxlway.com", "https://www.voxlway.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Sync-Key"],
)

@app.get("/health")
def read_health():
    """
    Verify that the API is running.
    """
    return {"status": "ok"}
