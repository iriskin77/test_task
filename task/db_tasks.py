from datetime import datetime
from task.models import Task, Product
from task.schema import TaskFilter, TaskGetPostPatch, ListTasksAdd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, update, delete
from fastapi import HTTPException


# ==================Post endpoint. Create a task==================


async def _create_task(item: ListTasksAdd, async_session: AsyncSession):

    res_list = []
    for new_task in item.tasks:

        task = await get_task_by_batch_date(new_task=new_task,
                                            async_session=async_session)

        # Если смена не закрыта (False)
        if not new_task.is_closed:
            new_task.closed_at = None

        # Если уже существует какая-то партия с аналогичным номером партии и датой партии, мы должны ее перезаписать.
        # Здесь проверяем, если есть, то перезаписываем
        if task is not None:

            new_task_to_update = new_task.dict(exclude={'number_batch', 'date_batch'})

            query = update(Task).\
                where(and_(Task.number_batch == task.number_batch,
                           Task.date_batch == task.date_batch)).values(**new_task_to_update)

            res_list.append(new_task)
            await async_session.execute(query)

        else:
            new_task_to_add = Task(**new_task.dict())
            async_session.add(new_task_to_add)
            res_list.append(new_task)

    await async_session.commit()
    return {'tasks': res_list}


async def get_task_by_batch_date(new_task: TaskGetPostPatch,
                                 async_session: AsyncSession):

    query = select(Task).where(and_(Task.number_batch == new_task.number_batch,
                                    Task.date_batch == new_task.date_batch))

    task = await async_session.execute(query)
    task_row = task.fetchone()
    if task_row is not None:
        return task_row[0]


# ==================Get endpoint. Get a task by id ==================


async def _get_task(id: int, async_session: AsyncSession):

    try:

        task = await _get_task_by_id(id=id,
                                     async_session=async_session)

        products_query = select(Product).\
            select_from(Task).\
            join(Product, Product.number_batch_id == Task.number_batch).\
            where(Product.number_batch_id == task.number_batch)

        products = await async_session.execute(products_query)

        pr = [p for p in products.scalars()]

        res = {
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

        return res

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex}")


async def _get_task_by_id(id: int, async_session: AsyncSession):

    query = select(Task).where(Task.id == id)
    task = await async_session.execute(query)
    task_row = task.fetchone()
    if task_row is not None:
        return task_row[0]


# ================ Patch endpoint, Change a task =================


async def _change_task(id: int,
                       params_to_update: dict,
                       async_session: AsyncSession):

    is_closed = params_to_update.get('is_closed', None)

    # Если статус закрытия партии меняется на True, то в closed_at необходимо выставить текущий datetime
    if is_closed is not None and is_closed:
        params_to_update['closed_at'] = datetime.now()

    # если наоборот -- то null
    if is_closed is not None and not is_closed:
        params_to_update['closed_at'] = None

    query = update(Task).\
        where(Task.id == id).\
        values(**params_to_update)

    task_updated = await async_session.execute(query)
    await async_session.commit()

    task_updated = await _get_task_by_id(id=id,
                                         async_session=async_session)

    return task_updated


# ======================== Filter tasks ==========================

async def _get_filtered_tasks(item: TaskFilter,
                              offset: int,
                              limit: int,
                              async_session: AsyncSession):

    params_to_sort = item.dict(exclude_none=True)
    try:
        query = select(Task).\
            filter_by(**params_to_sort).offset(offset).limit(limit)

        tasks = await async_session.execute(query)
        res_tasks = [task for task in tasks.scalars()]
        res = {"tasks": res_tasks}
        return res

    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"{ex}")
