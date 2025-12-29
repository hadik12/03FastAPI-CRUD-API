from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    in_stock: bool = True


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    in_stock: Optional[bool] = None


class ItemResponse(ItemBase):
    id: int
    created_at: datetime

    # Pydantic v2 replacement for orm_mode=True
    model_config = ConfigDict(from_attributes=True)
