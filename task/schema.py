from typing import List, Optional
from product.schema import ProductBase
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime, date


class TaskGetPostPatch(BaseModel):
    is_closed: bool | None = Field(validation_alias="СтатусЗакрытия", default=True)
    closed_at: Optional[datetime] | None = Field(validation_alias="ВремяЗакрытия", default=None)
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


class ListTasksAdd(BaseModel):
    tasks: List[TaskGetPostPatch]


class TaskProducts(TaskGetPostPatch):
    products: List[ProductBase]


class TaskChange(BaseModel):
    is_closed: Optional[bool] | None
    task: str | None
    line: str | None
    shift: str | None
    group: str | None
    number_batch: int | None
    date_batch: date | None
    nomenclature: str | None
    code: str | None
    index: str | None
    date_begin: datetime | None
    date_end: datetime | None


class TaskFilter(BaseModel):
    task: Optional[str] = None
    line: Optional[str] = None
    shift: Optional[str] = None
    group: Optional[str] = None
    number_batch: Optional[int] = None


class TaskFilterRes(BaseModel):
    tasks: List[TaskGetPostPatch] | None = None
