import os

import httpx
from fastapi import FastAPI, HTTPException, Depends

from src.api_proxy.auth import verify_internal_key

app = FastAPI()
WISE_API_TOKEN = os.getenv("WISE_API_TOKEN")
MONOBANK_TOKEN = os.getenv("MONOBANK_TOKEN")


@app.get("/monobank")
async def monobank():
    async with httpx.AsyncClient(timeout=5) as c:
        r = await c.get("https://api.monobank.ua/bank/currency")

        if r.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit from Monobank API")

        r.raise_for_status()
        return r.json()

@app.get("/monobank/client", dependencies=[Depends(verify_internal_key)])
async def monobank_client_info():
    if not MONOBANK_TOKEN:
        raise HTTPException(500, "Token not configured")
    headers = {"X-Token": MONOBANK_TOKEN}

    async with httpx.AsyncClient(timeout=5) as c:
        r = await c.get(
            "https://api.monobank.ua/personal/client-info",
            headers=headers
        )

        if r.status_code == 429:
            raise HTTPException(status_code=429, detail="Rate limit from Monobank API")

        r.raise_for_status()
        return r.json()

@app.get("/wise")
async def wise():
    if not WISE_API_TOKEN:
        raise HTTPException(500, "Token not configured")
    async with httpx.AsyncClient(timeout=5) as c:
        headers = {"Authorization": f"Bearer {WISE_API_TOKEN}"}
        print(headers)
        r = await c.get("https://api.wise.com/v1/rates?source=USD&target=GBP", headers=headers)
        r.raise_for_status()
        return r.json()
