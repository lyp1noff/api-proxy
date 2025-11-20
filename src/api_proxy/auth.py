import os
from fastapi import Header, HTTPException, status

INTERNAL_KEY = os.getenv("INTERNAL_API_KEY", "super-secret-key")  # default


async def verify_internal_key(x_internal_key: str = Header(None)):
    if x_internal_key != INTERNAL_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing internal API key"
        )