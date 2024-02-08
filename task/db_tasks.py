from datetime import datetime
from task.models import Task, Product
from task.schema import TaskBase, TaskFilter, TaskProducts
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from fastapi import HTTPException


# ==================Post endpoint. Create a task==================


async def _create_task(item: TaskBase, async_session: AsyncSession):

    task_check = await get_task_by_batch_date(number_batch=item.number_batch,
                                              date_batch=item.date_batch,
                                              async_session=async_session)

    if task_check is not None:
        query = delete(Task).where(and_(Task.number_batch == item.number_batch, item.date_batch))
        await async_session.execute(query)

    try:

        new_task = Task(**item.dict())

        async_session.add(new_task)
        await async_session.commit()

        return new_task

    except Exception as ex:
        HTTPException(status_code=500, detail=f"Invalid insert to the database {ex}")


async def get_task_by_batch_date(number_batch: int, date_batch: datetime, async_session: AsyncSession):
    query = select(Task).where(and_(Task.number_batch == number_batch, Task.date_batch == date_batch))
    task = await async_session.execute(query)
    return task


# ==================Get endpoint. Get a task by id ==================


async def _get_task(id: int, async_session: AsyncSession):

    try:

        query = select(Task).where(Task.id == id)
        task_extraced = await async_session.execute(query)
        task = task_extraced.fetchone()[0]

        products_query = select(Product).where(Product.number_batch_id == task.number_batch)
        products = await async_session.execute(products_query)

        if products is None:
            HTTPException(status_code=404, detail="Products with this batch were not found")

        pr = [elem for elem in products.scalars()]

        res = {
              "id": task.id,
              "is_closed": task.is_closed,
              "closed_at": task.closed_at,
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
              "products": pr
        }

        #res1 = {**task.dict(), "products": rs}

        return res

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex}")


async def _get_task_by_id(id: int, async_session: AsyncSession):

    task = select(Task).where(Task.id == id)

    if task is None:
        HTTPException(status_code=404, detail="Task with this id was not found")

    res = await async_session.execute(task)
    return res.fetchone()[0]


# ================ Patch endpoint, Change a task =================


async def _change_task(id: int, params_to_update: dict, async_session: AsyncSession):
    query = update(Task).where(Task.id == id).values(**params_to_update)
    task_updated = await async_session.execute(query)
    await async_session.commit()
    #return task_updated
    task_updated_row = task_updated.fetchone()

    if task_updated_row[0] is None:
        HTTPException(status_code=404, detail="Task with this id was not found")

    return task_updated_row[0]


# ======================== Filter tasks ==========================

async def _filter_tasks(item: TaskFilter, offset: int, limit: int, async_session: AsyncSession):
    params_to_sort = item.dict(exclude_none=True)
    try:
        query = select(Task).filter_by(**params_to_sort).offset(offset).limit(limit)
        tasks = await async_session.execute(query)
        res_tasks = [i for i in tasks.scalars()]
        res = {"tasks": res_tasks}
        return res

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex}")
