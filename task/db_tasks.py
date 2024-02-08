from datetime import datetime
from task.models import Task, Product
from task.schema import TaskBase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from fastapi import HTTPException


async def _get_batch(id: int, async_session: AsyncSession):

    try:
        query = select(Task).where(Task.id == id)
        task_extraced = await async_session.execute(query)
        task = task_extraced.fetchone()[0]

        products_query = select(Product).where(Product.number_batch_id == task.number_batch)
        products = await async_session.execute(products_query)

        if products is None:
            HTTPException(status_code=404, detail="Products with this batch is were not found")

        res = {
              "id": task.id,
              "status": task.status,
              "task": task.task,
              "line": task.line,
              "shift": task.shift,
              "group": task.group,
              "number_batch": task.number_batch,
              "date_batch": task.date_batch,
              "nomenclature": task.nomenclature,
              "code": task.code,
              "index": task.index,
              "date_begin": task.date_begin,
              "date_end": task.date_end,
              "products": products.scalars()
        }

        return res

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex}")


async def get_task_by_batch_date(number_batch: int, date_batch: datetime, async_session: AsyncSession):
    query = select(Task).where(and_(Task.number_batch == number_batch, Task.date_batch == date_batch))
    task = await async_session.execute(query)
    return task
