from typing import List, Optional
from product.schema import ProductBase
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, date


class TaskBase(BaseModel):
    is_closed: bool | None = Field(validation_alias="СтатусЗакрытия")
    closed_at: datetime | None = Field(validation_alias="ВремяЗакрытия")
    task: str | None = Field(validation_alias="ПредставлениеЗаданияНаСмену")
    line: str | None = Field(validation_alias="Линия")
    shift: str | None = Field(validation_alias="Смена")
    group: str | None = Field(validation_alias="Бригада")
    number_batch: int | None = Field(validation_alias="НомерПартии")
    date_batch: date | None = Field(validation_alias="ДатаПартии")
    nomenclature: str | None = Field(validation_alias="Номенклатура")
    code: str | None = Field(validation_alias="КодЕКН")
    index: str | None = Field(validation_alias="ИдентификаторРЦ")
    date_begin: datetime | None = Field(validation_alias="ДатаВремяНачалаСмены")
    date_end: datetime | None = Field(validation_alias="ДатаВремяОкончанияСмены")

    model_config = ConfigDict(populate_by_name=True,)


class TaskProducts(TaskBase):
    products: List[ProductBase]


class TaskChange(TaskBase):
    is_closed: bool = Field(exclude=True)
    closed_at: datetime = Field(exclude=True)


class TaskChangeReturn(BaseModel):
    id: int


class TaskFilter(BaseModel):
    task: Optional[str] | None = None
    line: Optional[str] | None = None
    shift: Optional[str] | None = None
    group: Optional[str] | None = None
    number_batch: Optional[int] | None = None


class TaskFilterRes(BaseModel):
    tasks: List[TaskBase] | None = None
