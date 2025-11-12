import httpx
from backend.core.config import settings

from typing import Any

from backend.models.users import Users


GITHUB_API_BASE = "https://api.github.com"


async def fetch_github_user(usernames: Users) -> dict[str, Any]:
    """
    Fetch GitHub user details by username(s)

    Args:
        usernames (Users): Pydantic model containing a list of GitHub usernames.
    Returns:
        dict[str, Any]: A dictionary with usernames as keys and their profile data or error messages as values.
    """

    results = {}
    for username in usernames.usernames:
        headers = {"Accept": "application/vnd.github+json"}
        if settings.GITHUB_TOKEN:
            headers["Authorization"] = f"token {settings.GITHUB_TOKEN}"

        url = f"{GITHUB_API_BASE}/users/{username}"
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
        if resp.status_code == 404:
            results[username] = {"message": "Not Found"}
        else:
            resp.raise_for_status()
            results[username] = resp.json()
    return results
