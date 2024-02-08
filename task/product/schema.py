from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):

    id: int
    unique_code: str
    number_batch_id: int
    date_product: datetime

    class Config:
        orm_mode = True

