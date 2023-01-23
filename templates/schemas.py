from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    tax: Optional[float] = None