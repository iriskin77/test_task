from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date


class ProductBase(BaseModel):

    id: int
    unique_code: str
    number_batch_id: int
    date_product: date

    class Config:
        orm_mode = True


class ProductAddTasks(BaseModel):

    products: List[ProductBase]


class ProductPost(ProductBase):

    is_aggregated: Optional[bool]
    aggregated_at: Optional[datetime]


class ProductAggregation(BaseModel):

    task_id: int
    unique_code: str

