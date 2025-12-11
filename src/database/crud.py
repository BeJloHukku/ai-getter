
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ChatRequest


async def get_user_requests(
        ip_address: str, 
        session: AsyncSession
) -> list[ChatRequest]:
    query = select(ChatRequest).filter_by(ip_address=ip_address)
    result = await session.execute(query)
    result = result.scalars().all()
    return result


async def add_request_data(
        ip_address: str, 
        prompt: str, 
        response: str, 
        session: AsyncSession,
) -> None:
    new_request = ChatRequest(
        ip_address=ip_address,
        prompt=prompt,
        response=response
    )

    session.add(new_request)
    await session.commit()
    
