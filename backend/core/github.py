# backend/core/github.py
import httpx

async def fetch_github_profile(username: str):
    url = f"https://api.github.com/users/{username}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            return {"error": "User not found"}
        return resp.json()
