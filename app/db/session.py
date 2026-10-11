from typing import Annotated, AsyncIterator
from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
    )
from app.core.config import get_settings



settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    connect_args={
    "server_settings": {"search_path": settings.DB_SCHEMA},
    },
)



SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncIterator[AsyncSession]:
 async with SessionLocal() as session:
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise



# Use for regular API endpoints. Requires a FastAPI version that supports
# dependency scope="function".
SessionDep = Annotated[
    AsyncSession,
    Depends(get_session, scope="function"),
]
    


# Use only for StreamingResponse endpoints that access the database while
# the response is streaming.
StreamingSessionDep = Annotated[
    AsyncSession,
    Depends(get_session),
]

