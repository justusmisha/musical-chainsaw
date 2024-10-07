from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from typing import List, Sequence, Optional

from BotRouter.app.db.models import Class


async def get_class_by_number(db: AsyncSession, class_number) -> Sequence[Class]:
    """
    Retrieve class by number from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        class_number (int): The asynchronous database session.

    Returns:
        List[SchoolActivity]: A list of SchoolActivity objects.
    """
    async with db.begin():
        result = await db.execute(select(Class).where(Class.class_number == class_number))
        activities = result.scalars().first()

    return activities


async def get_class_by_grad(db: AsyncSession, grad: str) -> Sequence[Class]:
    """
    Retrieve all classes by grad from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        grad (str): Value of class classification.

    Returns:
        List[Class]: A list of Class objects.
    """
    if grad == 'elementary':
        scope = [1, 2, 3, 4]
    elif grad == 'middle':
        scope = [5, 6, 7, 8, 9]
    elif grad == 'high':
        scope = [10, 11]
    else:
        return []

    async with db.begin():
        result = await db.execute(select(Class).where(Class.class_number.in_(scope)))
        activities = result.scalars().all()

    return activities
