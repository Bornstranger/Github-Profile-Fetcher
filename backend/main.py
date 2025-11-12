from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models.users import Users
from .utils.github_fetcher import fetch_github_user

# Create FastAPI app
app = FastAPI(
    title="GitHub Profile Fetcher API",
    description="Fetch any GitHub user's public profile details safely via FastAPI backend.",
    version="1.0.0",
)

# Enable CORS (so your frontend can call this API locally)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL (e.g., "http://localhost:3000")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Route
@app.get("/")
def root():
    return {"message": "GitHub Profile Fetcher API is running successfully 🚀"}


# Route to fetch GitHub user details
@app.post("/users/")
async def get_github_user(usernames: Users):
    """Fetch a GitHub user's public profile information"""
    data = await fetch_github_user(usernames)

    return data
