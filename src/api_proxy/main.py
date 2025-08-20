import os

import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()
WISE_API_TOKEN = os.getenv("WISE_API_TOKEN")


@app.get("/monobank")
async def monobank():
    async with httpx.AsyncClient(timeout=5) as c:
        r = await c.get("https://api.monobank.ua/bank/currency")
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
