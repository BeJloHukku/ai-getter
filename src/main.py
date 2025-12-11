from fastapi import FastAPI, Body, Request
from contextlib import asynccontextmanager

from src.database.crud import get_user_requests
from src.database.db import engine
from src.database.models import Base
from src.gemini_client import get_answer_from_gemini


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/requests")
async def get_my_requests(request: Request):
    ip_address = request.client.host
    print(f"{ip_address=}")
    user_requests = await get_user_requests(ip_address=ip_address)
    return user_requests


@app.post("/requests")
async def send_prompt(
        prompt: str = Body(embed=True),
):
    answer = await get_answer_from_gemini(prompt)
    return {"data": answer}
