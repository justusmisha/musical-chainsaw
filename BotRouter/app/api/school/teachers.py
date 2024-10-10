from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from BotRouter.app.db.functions.classes import get_class_by_number, get_class_by_grad
from BotRouter.app.db.functions.get_session import get_async_session
from BotRouter.app.db.functions.teachers import get_teachers_by_class, get_all_teachers
from BotRouter.app.schemas.activ import TeacherSm
from BotRouter.app.schemas.classes import SchoolClass

router = APIRouter()


@router.get('/{class_number}', response_model=Sequence[TeacherSm])
async def get_teachers_by_class_num(class_number: int, db: AsyncSession = Depends(get_async_session)):
    teachers = await get_teachers_by_class(db=db, class_number=class_number)
    return teachers


@router.get('/all/teachers')
async def get_all_teachers_from_db(db: AsyncSession = Depends(get_async_session)):
    teachers = await get_all_teachers(db=db)
    return teachers

