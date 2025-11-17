# backend/main.py
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis.asyncio as aioredis
import logging
from backend.core.github import fetch_github_profile

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------------------
# Redis connection
# -----------------------------
# Make sure Redis is running at localhost:6379
redis_client = aioredis.from_url("redis://localhost:6379/0", decode_responses=True)

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="GitHub Profile Fetcher")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Rate limiter dependency
# -----------------------------
async def rate_limiter(request: Request):
    """
    Limit 2 requests per minute per IP.
    """
    ip = request.client.host
    key = f"rate_limit:{ip}"
    
    # Increment the counter
    count = await redis_client.incr(key)
    
    if count == 1:
        # First request, set TTL 60s
        await redis_client.expire(key, 60)
    
    if count > 2:
        # More than 2 requests in current minute
        raise HTTPException(status_code=429, detail="Wait for a minute before retrying.")

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
async def root():
    return {"status": "ok", "message": "GitHub Profile Fetcher API"}

@app.get("/api/github/{username}")
async def get_github_user(
    username: str,                  # Path parameter
    request: Request,
    _: None = Depends(rate_limiter)  # Inject rate limiter
):
    profile = await fetch_github_profile(username)
    if "error" in profile:
        raise HTTPException(status_code=404, detail="User not found")
    return profile

# -----------------------------
# Optional: shutdown Redis properly
# -----------------------------
@app.on_event("shutdown")
async def shutdown():
    await redis_client.close()
    await redis_client.connection_pool.disconnect()
