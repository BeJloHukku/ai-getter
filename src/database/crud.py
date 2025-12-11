from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ChatRequest


async def get_user_requests(ip_address: str, session: AsyncSession) -> list[ChatRequest]:
    query = select(ChatRequest).filter_by(ip_address=ip_address)
    result = await session.execute(query)
    result = result.scalars().all()
    return result
