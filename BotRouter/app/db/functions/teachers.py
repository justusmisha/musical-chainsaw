from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from typing import List, Sequence, Optional

from BotRouter.app.db.models import Teacher, ClassTeacher, Class


async def get_teachers_by_class(db: AsyncSession, class_number: int) -> Sequence[Teacher]:
    """
    Retrieve teachers for a given class number from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        class_number (int): The class number to retrieve teachers for.

    Returns:
        List[Teacher]: A list of Teacher objects.
    """
    async with db.begin():
        # Join ClassTeacher with Teacher and Class to get teachers for the given class number
        result = await db.execute(
            select(Teacher)
            .join(ClassTeacher, Teacher.id == ClassTeacher.teacher_id)
            .join(Class, Class.id == ClassTeacher.class_id)
            .where(Class.class_number == class_number)
        )
        teachers = result.scalars().all()

    return teachers


async def get_all_teachers(db: AsyncSession) -> Sequence[Teacher]:
    """
    Retrieve teachers for a given class number from the database.

    Args:
        db (AsyncSession): The asynchronous database session.
    Returns:
        List[Teacher]: A list of Teacher objects.
    """
    async with db.begin():
        result = await db.execute(select(Teacher))
        teachers = result.scalars().all()

    return teachers

