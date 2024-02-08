from datetime import datetime
from task.models import Task, Product
from task.schema import TaskBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from fastapi import HTTPException


async def _create_task(item: TaskBase, async_session: AsyncSession):

    task_check = await get_task_by_batch_date(number_batch=item.number_batch,
                                              date_batch=item.date_batch,
                                              async_session=async_session)

    if task_check is not None:
        query = delete(Task).where(and_(Task.number_batch == item.number_batch, item.date_batch))
        await async_session.execute(query)

    try:
        new_task = Task(
                 status=item.status,
                 task=item.task,
                 line=item.line,
                 shift=item.shift,
                 group=item.group,
                 number_batch=item.number_batch,
                 date_batch=item.date_batch,
                 nomenclature=item.nomenclature,
                 code=item.code,
                 index=item.index,
                 date_begin=item.date_begin,
                 date_end=item.date_end)

        # new_task = Task(**item.dict())

        async_session.add(new_task)
        await async_session.commit()
        return new_task

    except Exception as ex:
        HTTPException(status_code=500, detail=f"Invalid insert to the database {ex}")


async def get_task_by_batch_date(number_batch: int, date_batch: datetime, async_session: AsyncSession):
    query = select(Task).where(and_(Task.number_batch == number_batch, Task.date_batch == date_batch))
    task = await async_session.execute(query)
    return task
