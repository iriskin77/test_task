from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from task import db_tasks
from task.schema import TaskProducts, TaskChange, TaskFilter, TaskFilterRes, TaskGetPostPatch, ListTasksAdd


router_task = APIRouter()


@router_task.post("/", response_model=ListTasksAdd)
async def create_task(item: ListTasksAdd,
                      async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт добавления сменных заданий"""""

    try:
        res = await db_tasks._create_task(item=item,
                                          async_session=async_session)

        return res
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Database error: {ex}")


@router_task.get("/{id}", response_model=TaskProducts)
async def get_task(id: int,
                   async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт получения сменного задания (партии) по ID (primary key)"""""

    task = await db_tasks._get_task_by_id(id=id,
                                          async_session=async_session)

    # Если сменного задания с данным ID нет, то вернуть 404 ошибку.
    if task is None:
        raise HTTPException(status_code=404,
                            detail="Task with this id was not found")

    try:
        res = await db_tasks._get_task(id=id,
                                       async_session=async_session)

        return res
    except Exception as ex:
        raise HTTPException(status_code=500,
                            detail=f"Database error: {ex}")


@router_task.patch("/{id}", response_model=TaskGetPostPatch)
async def change_task(id: int,
                      params_to_update: TaskChange,
                      async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт изменения сменного задания (партии) по ID (primary key)"""""

    task = await db_tasks._get_task_by_id(id=id,
                                          async_session=async_session)

    if task is None:
        HTTPException(status_code=404, detail="Not found")

    if params_to_update == {}:
        raise HTTPException(status_code=422,
                            detail="At least one parameter for user update info should be provided")

    params = params_to_update.dict(exclude_none=True)

    try:
        res = await db_tasks._change_task(id=id,
                                          params_to_update=params,
                                          async_session=async_session)

        return res
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Database error: {ex}")


@router_task.get("/filter/{item}", response_model=TaskFilterRes)
async def get_filtered_tasks(item: TaskFilter = Depends(),
                             offset: int = 0,
                             limit: int = 10,
                             async_session: AsyncSession = Depends(get_async_session)):

    if item == {}:
        raise HTTPException(status_code=422,
                            detail="At least one parameter should be provided")

    res = await db_tasks._get_filtered_tasks(item=item,
                                             limit=limit,
                                             offset=offset,
                                             async_session=async_session)
    return res
