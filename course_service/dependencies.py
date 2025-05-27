# dependencies.py

import httpx
from fastapi import Depends, HTTPException, status, Request
from uuid import UUID

# Replace with actual Django service endpoint
USER_SERVICE_URL = "http://localhost:8000/api/user/me/me/"

async def get_current_user_id(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization Header")

    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get(USER_SERVICE_URL, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Could not fetch user info")

    user_data = response.json()
    print("User data from Django:", user_data)  # For quick local testing

    try:
        user_uuid = UUID(str(user_data["username"]))  # ✅ safer, ensures it's parsed from string
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid user UUID format")

    return user_uuid
