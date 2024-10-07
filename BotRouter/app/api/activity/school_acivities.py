from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from BotRouter.app.db.functions.get_session import get_async_session
from BotRouter.app.db.functions.school_activ import get_activities, db_activity_by_name
from BotRouter.app.schemas.activ import SchoolActivitySm

router = APIRouter()


@router.get("/all")
async def read_activities(db: AsyncSession = Depends(get_async_session)):
    activities = await get_activities(db)
    return activities


@router.get("/by_name", response_model=SchoolActivitySm)
async def get_acivity_by_name(name: str, db: AsyncSession = Depends(get_async_session)):
    activity = await db_activity_by_name(name, db)
    if activity:
        return SchoolActivitySm.from_orm(activity)
    return None
