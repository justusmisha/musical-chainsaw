from pydantic import BaseModel


class AdditClasses(BaseModel):
    name: str
    price: int
    schedule: str
