from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from BotRouter.app.data.config import DATABASE_URL

# Create the database engine
engine = create_async_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session