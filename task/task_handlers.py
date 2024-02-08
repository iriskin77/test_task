from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from task import db_tasks
from task.schema import TaskBase


router_task = APIRouter()


@router_task.post("/", response_model=TaskBase)
async def create_task(item: TaskBase, async_session: AsyncSession = Depends(get_async_session)):
    """"Эндпойнт добавления сменных заданий"""""
    try:
        res = await db_tasks._create_task(item=item, async_session=async_session)
        return res
    except Exception as ex:
        HTTPException(status_code=500, detail=f"Database error: {ex}")


