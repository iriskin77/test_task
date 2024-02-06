from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router_batch = APIRouter()


@router_batch.get("/")
async def get_batch():
    pass


@router_batch.patch("/")
async def change_batch():
    pass
