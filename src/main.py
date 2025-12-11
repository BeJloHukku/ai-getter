from typing import Annotated, AsyncGenerator
from fastapi import FastAPI, Body, Request, Depends, HTTPException, status
from contextlib import asynccontextmanager

from src.exeptions import AiGeminiError, NoResponseWasGivenFromGeminiError
from src.database.crud import add_request_data, get_user_requests
from src.database.db import engine
from src.database.models import Base
from src.gemini_client import get_answer_from_gemini
from src.database.db import new_session

from sqlalchemy.ext.asyncio import AsyncSession


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


app = FastAPI(lifespan=lifespan)


@app.get("/requests")
async def get_my_requests(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_session)]
):
    ip_address = request.client.host
    print(f"{ip_address=}")
    user_requests = await get_user_requests(
        ip_address=ip_address, 
        session=session
    )
    return user_requests


@app.post("/requests")
async def send_prompt(
        request: Request,
        prompt: Annotated[str, Body(embed=True)],
        session: Annotated[AsyncSession, Depends(get_session)]
):
    ip_address = request.client.host
    try:
        response = await get_answer_from_gemini(prompt)
    except NoResponseWasGivenFromGeminiError:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Ошибка генерирования ответа! Попробуйте еще раз!",
        )
    except AiGeminiError:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Сервис Gemini не доступен, попробуйте позже!",
        )

    await add_request_data(ip_address, prompt, response, session)
    return {"data": response}
