from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean, Date, TIMESTAMP
from sqlalchemy.orm import relationship, backref
from core.base import Base


class Task(Base):

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    is_closed = Column(Boolean, nullable=True) # "СтатусЗакрытия": false,
    closed_at = Column(TIMESTAMP)
    task = Column(String) # "ПредставлениеЗаданияНаСмену": "Задание на смену 2345",
    line = Column(String) # "Линия": "Т2",
    shift = Column(String) # "Смена": "1",
    group = Column(String) # "Бригада": "Бригада №4",
    number_batch = Column(Integer, unique=True) # "НомерПартии": 22222,
    date_batch = Column(Date, unique=True) # "ДатаПартии": "2024-01-30",
    nomenclature = Column(Text) # "Номенклатура": "Какая то номенклатура",
    code = Column(String) # "КодЕКН": "456678",
    index = Column(String) # "ИдентификаторРЦ": "A",
    date_begin = Column(TIMESTAMP) # "ДатаВремяНачалаСмены": "2024-01-30T20:00:00+05:00",
    date_end = Column(TIMESTAMP) # "ДатаВремяОкончанияСмены": "2024-01-31T08:00:00+05:00"


class Product(Base):

    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    unique_code = Column(String, unique=True)
    number_batch_id = Column(Integer, ForeignKey("task.number_batch"))  #"НомерПартии": 22222,
    number_batch = relationship("Task")
    is_aggregated = Column(Boolean, nullable=True)
    aggregated_at = Column(TIMESTAMP, nullable=True)
    date_product = Column(TIMESTAMP) #"ДатаПартии": "2024-01-30"

