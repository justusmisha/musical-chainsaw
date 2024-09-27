from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()


@router.get('/user/{user_id}')
async def get_user_endpoint(user_id: str):
    """
    Эндпоинт для получения информации о пользователе по идентификатору пользователя.

    :param user_id: Идентификатор пользователя.
    :param db: Асинхронная сессия базы данных.
    :return: Информация о пользователе в виде Pydantic-схемы.
    """
    return await get_user(user_id, db)
