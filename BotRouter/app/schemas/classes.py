from typing import Dict, Optional

from pydantic import BaseModel


class SchoolClass(BaseModel):
    id: int
    max_places: int
    left_places: int
    min_age: int
    max_age: int
    price: int
    schedule: Dict[str, str]
    class_number: int

    class Config:
        orm_mode = True
        from_attributes = True