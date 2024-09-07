from typing import List, Optional
from pydantic import BaseModel

from ..items.schemas import Item

class StoreBase(BaseModel):
    name: str


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    items: List[Item] = []

    class config:
        orm_mode = True
