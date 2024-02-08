from pydantic import BaseModel
from datetime import datetime, date


class TaskBase(BaseModel):
    id: int | None = None
    is_closed: bool | None = None
    closed_at: datetime | None = None
    task: str | None = None
    line: str | None = None
    shift: str | None = None
    group: str | None = None
    number_batch: int | None = None
    date_batch: date | None = None
    nomenclature: str | None = None
    code: str | None = None
    index: str | None = None
    date_begin: datetime | None = None
    date_end: datetime | None = None

    class Config:
        orm_mode = True
