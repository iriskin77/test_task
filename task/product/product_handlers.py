from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router_product = APIRouter()


@router_product.get("/")
def add_product():
    pass
