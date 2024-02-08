from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from task import db_tasks
from task.schema import TaskBase, TaskProducts, TaskChange


router_task = APIRouter()


@router_task.post("/", response_model=TaskBase)
async def create_task(item: TaskBase, async_session: AsyncSession = Depends(get_async_session)):
    """"Эндпойнт добавления сменных заданий"""""
    try:
        res = await db_tasks._create_task(item=item, async_session=async_session)
        return res
    except Exception as ex:
        HTTPException(status_code=500, detail=f"Database error: {ex}")


@router_task.get("/{id}", response_model=TaskProducts)
async def get_batch(id: int, async_session: AsyncSession = Depends(get_async_session)):
    """"Эндпойнт получения сменного задания (партии) по ID (primary key)"""""

    task = db_tasks._get_task_by_id(id=id, async_session=async_session)
    if task is None:
        HTTPException(status_code=404, detail="Task with this id was not found")

    try:
        res = await db_tasks._get_batch(id=id, async_session=async_session)
        return res
    except Exception as ex:
        HTTPException(status_code=500, detail=f"Database error: {ex}")


@router_task.patch("/{id}", response_model=TaskChange)
async def change_batch(id: int, params_to_update: TaskChange, async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт изменения сменного задания (партии) по ID (primary key)"""""

    task = await db_tasks._get_task_by_id(id=id, async_session=async_session)
    if task is None:
        HTTPException(status_code=404, detail="Not found")

    if params_to_update == {}:
        raise HTTPException(status_code=422, detail="At least one parameter for user update info should be provided")

    params = params_to_update.dict(exclude_none=True)

    try:
        res = await db_tasks.change_batch(id=id, params_to_update=params, async_session=async_session)
        return res
    except Exception as ex:
        HTTPException(status_code=500, detail=f"Database error: {ex}")
