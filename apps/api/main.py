from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import search
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from limiter import limiter

app = FastAPI(title="API")

app.include_router(search.router, prefix="/api/v1")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def read_health():
    """
    Verify that the API is running.
    """
    return {"status": "ok"}
