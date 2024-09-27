from datetime import timedelta
from typing import Optional, List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from BotRouter.app.schemas.addit_classes import AdditClasses
from BotRouter.app.logger import logger


async def get_user(user_id: str, db: AsyncSession) -> Optional[AdditClasses]:
    """
    Получает информацию о пользователе по идентификатору пользователя.

    :param user_id: Идентификатор пользователя.
    :param db: Асинхронная сессия базы данных.
    :return: Pydantic-схема с информацией о пользователе или None.
    """
    try:
        # Выполняем запрос для получения пользователя
        result = await db.execute(
            select(Users).where(Users.user_id == user_id)
        )

        # Получаем результат
        user = result.scalars().first()

        if not user:
            logger.error(f"User {user_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Преобразуем объект SQLAlchemy в Pydantic-схему
        return UserSchema.from_orm(user)
    except SQLAlchemyError as e:
        logger.error(f"Failed to fetch user for user_id {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Iternal server Error")