import json
from typing import Dict, Optional

from pydantic import BaseModel

from BotRouter.app.db.models import Teacher


class TeacherSm(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    experience: int
    description: str


class SchoolActivitySm(BaseModel):
    name: str
    id: int
    teacher_id: int
    min_age: int
    max_age: int
    schedule: Dict[str, str]
    prices: Dict[str, int]
    contact_number: str

    class Config:
        orm_mode = True
        # arbitrary_types_allowed = True
        # orm_mode = True
        from_attributes = True
