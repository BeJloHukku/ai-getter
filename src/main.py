from fastapi import FastAPI, Body
from contextlib import asynccontextmanager

from src.db import engine
from src.models import Base
from src.gemini_client import get_answer_from_gemini


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/requests")
async def get_my_requests():
    return "Hello world"


@app.post("/requests")
async def send_prompt(
        prompt: str = Body(embed=True),
):
    answer = await get_answer_from_gemini(prompt)
    return {"data": answer}
