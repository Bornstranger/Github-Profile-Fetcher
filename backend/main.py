from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from pathlib import Path

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
@app.get("/user/{username}")
async def get_github_user(username: str):
    """Fetch a GitHub user's public profile information"""
    data = await fetch_github_user(username)

    # If GitHub returns an error (like user not found)
    if "message" in data and data["message"].lower() == "not found":
        raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")

    return data


# If a frontend directory exists at repo root, mount it at /static and provide a small UI endpoint
FRONTEND_DIR = Path(__file__).resolve().parents[1] / "frontend"
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/ui")
def ui():
    """Return the frontend `index.html` when available (convenience for local dev)."""
    index = FRONTEND_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    return {"message": "Frontend not found. Place static files in ../frontend."}
