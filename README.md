# GitHub Profile Fetcher

Lightweight web app that fetches and displays public GitHub profile information.
It consists of a FastAPI backend (fetches data from the GitHub REST API) and a tiny static frontend (HTML/JS/CSS) that calls the API.

## Repository layout

```
Dockerfile
README.md
run.sh                 # convenience script to run backend locally
backend/               # FastAPI backend
  main.py              # FastAPI app and routes
  requirements.txt
  core/
    config.py          # settings (loads .env)
  utils/
    github_fetcher.py  # logic that calls GitHub API
frontend/              # static frontend
  index.html
  script.js
  style.css
```

## Quick overview

- Backend: FastAPI app exposing:
  - `GET /` — health check
  - `GET /user/{username}` — returns public GitHub user JSON
- Frontend: static page (`frontend/index.html`) that queries the backend and renders a small profile card.
- Config: backend loads environment variables from `backend/.env` (see below). An optional `GITHUB_TOKEN` can be provided to increase GitHub API rate limits.

## Requirements

- Docker (if using Docker)
- Or Python 3.11+ and pip to run locally

## Linting with ruff

This project includes a `pyproject.toml` with `ruff` configuration. Use `ruff` to lint and optionally fix issues.

Install ruff (recommended in the repo virtualenv or globally):

```powershell
pip install ruff
```

Run ruff checks from the repository root (it will read `pyproject.toml`):

```powershell
ruff check .
```

Run ruff to automatically fix many issues (safe fixes only):

```powershell
ruff check --fix .
```

Notes:
- The `pyproject.toml` in this repo sets a line length and a selection/ignore list for rules. Adjust that file if you want different behavior.
- If you use an editor integration (VS Code, Neovim, etc.) configure it to use the project's `ruff` settings.

## Local development (Python)

Recommended: create a virtual environment and run the backend with uvicorn.

From repository root (PowerShell):

```powershell
# create and activate venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell

# install dependencies
pip install -r backend/requirements.txt

# (optional) add a backend/.env file to set GITHUB_TOKEN
# backend/.env contents (example):
# GITHUB_TOKEN=ghp_yourtokenhere

# run backend (development, autoreload)
python -m uvicorn backend.main:app --reload
```

Notes:
- The backend uses `backend/core/config.py` which reads `.env` via pydantic-settings. Place `.env` inside the `backend/` folder.
- The frontend expects the API at `http://127.0.0.1:8000` by default (see `frontend/script.js`). If you change the host/port, update that file or serve the frontend from a host allowed by CORS.

## Using Docker

The included `Dockerfile` builds a small image that runs the backend with `uvicorn`.

Build the image (from repo root):

```powershell
docker build -t github-profile-fetcher:latest .
```

Run the container, mapping port 8000 and passing an env file:

```powershell
# run without token (public rate limits)
docker run --rm -p 8000:8000 github-profile-fetcher:latest

# or with an env file containing GITHUB_TOKEN
docker run --rm --env-file backend/.env -p 8000:8000 github-profile-fetcher:latest
```

Notes:
- The Docker image is based on `python:3.11-alpine` and copies `backend/` into `/code` and runs `uvicorn backend.main:app`.

## API

1. Health check

```http
GET /
Response:{ "message": "GitHub Profile Fetcher API is running successfully 🚀" }
```

2. Fetch GitHub user

```http
GET /user/{username}
Example: GET /user/octocat

Success: returns JSON object from GitHub user endpoint (same fields GitHub returns)
404: if GitHub returns `not found` the API responds with 404
```

Example curl (PowerShell):

```powershell
curl http://127.0.0.1:8000/user/octocat
```

The frontend (`frontend/index.html`) already calls this endpoint and displays avatar, name, bio, followers, repos and a link.

## Environment / Rate limits

- Without a token you are limited by GitHub's unauthenticated rate limits (~60 requests/hour per IP as of writing).
- You can provide a personal access token to increase rate limits. Create `backend/.env` with:

```
GITHUB_TOKEN=ghp_your_personal_access_token
```

The token is used in `backend/utils/github_fetcher.py` to set the Authorization header.

## Troubleshooting

- 401/403 from GitHub: check your `GITHUB_TOKEN` value and permissions. A simple public token without scopes is sufficient for public user data.
- Backend not reachable from frontend: ensure backend is running on `127.0.0.1:8000` (or update `frontend/script.js` API base). CORS is currently configured to allow all origins in `backend/main.py`.
- Docker build failing on Alpine: ensure Docker daemon has network access; pip installing wheels may require build dependencies for some packages (not expected for current requirements).

## Development notes / next steps

- Consider locking package versions in `backend/requirements.txt` for reproducible builds.
- Add a small `docker-compose.yml` if you want to run backend + a static server for the frontend together.
- Add tests for `github_fetcher.fetch_github_user` (happy path + user-not-found + timeout) to catch regressions.

## License

This repository does not include a license file. Add one if you intend to open-source the project.

---
If you want, I can:
- add a `docker-compose.yml` so frontend and backend can be served together, or
- add a simple automated test for `fetch_github_user` (uses httpx mock) and run it.
