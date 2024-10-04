from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from typing import List, Sequence, Optional

from BotRouter.app.db.models import SchoolActivity


async def get_activities(db: AsyncSession) -> Sequence[SchoolActivity]:
    """
    Retrieve all school activities from the database.

    Args:
        db (AsyncSession): The asynchronous database session.

    Returns:
        List[SchoolActivity]: A list of SchoolActivity objects.
    """
    async with db.begin():
        result = await db.execute(select(SchoolActivity))
        activities = result.scalars().all()

    return activities


async def db_activity_by_name(activ_name: str, db: AsyncSession) -> Optional[SchoolActivity]:
    """
    Retrieve all school activities with the specified name from the database.

    Args:
        activ_name (str): The name of the activity to filter by.
        db (AsyncSession): The asynchronous database session.

    Returns:
        Sequence[SchoolActivity]: A sequence of SchoolActivity objects that match the name.
    """
    async with db.begin():
        result = await db.execute(select(SchoolActivity).filter(SchoolActivity.name == activ_name))
        activity = result.scalar_one_or_none()

    return activity
