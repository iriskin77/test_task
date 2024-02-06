from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from core.base import Base


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    status = Column(Boolean) # "СтатусЗакрытия": false,
    task = Column(String) # "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
    line = Column(String) # "Линия": "Т2",
    shift = Column(String) # "Смена": "1",
    group = Column(String) # "Бригада": "Бригада №4",
    number_batch = Column(Integer, unique=True) # "НомерПартии": 22222,
    date_batch = Column(Date, unique=True) # "ДатаПартии": "2024-01-30",
    nomenclature = Column(Text) # "Номенклатура": "Какая то номенклатура",
    code = Column(String) # "КодЕКН": "456678",
    index = Column(String) # "ИдентификаторРЦ": "A",
    date_begin = Column(DateTime) # "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
    date_end = Column(DateTime) # "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00"


class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    number_batch = Column(Integer, ForeignKey("task.id"))
    number_batch_id = relationship("Task")
    date_product = Column(DateTime, unique=True)

