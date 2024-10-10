from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from BotRouter.app.db.functions.classes import get_class_by_number, get_class_by_grad
from BotRouter.app.db.functions.get_session import get_async_session
from BotRouter.app.schemas.classes import SchoolClass

router = APIRouter()


@router.get('/{class_number}', response_model=SchoolClass)
async def read_activities(class_number: int, db: AsyncSession = Depends(get_async_session)):
    school_class = await get_class_by_number(db=db, class_number=class_number)
    return school_class


@router.get('/grade/{grad}', response_model=List[SchoolClass])
async def read_activities(grad: str, db: AsyncSession = Depends(get_async_session)):
    school_classes = await get_class_by_grad(db=db, grad=grad)
    return school_classes
