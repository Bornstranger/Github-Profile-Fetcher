import httpx
from backend.core.config import settings

from typing import Any


GITHUB_API_BASE = "https://api.github.com"


async def fetch_github_user(username: str) -> dict[str, Any]:
# """Fetch public GitHub user data from GitHub REST API.


# Uses an optional token from settings for higher rate limits.
# Returns a dict with the GitHub user JSON response.
# Raises httpx.HTTPStatusError for 4xx/5xx responses.
# """
    headers = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_TOKEN:
        headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"


    url = f"{GITHUB_API_BASE}/users/{username}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()