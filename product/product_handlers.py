from core.async_session import get_async_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from product.schema import ListAddProducts, ProductAggregationRequest, ProductAggregationResponse
from product import db_products


router_product = APIRouter()


@router_product.post("/", response_model=ListAddProducts)
async def product_create(items: ListAddProducts,
                         async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт добавления продукции для сменного задания (партии)"""""

    try:
        res = await db_products._product_create(items=items,
                                                async_session=async_session)
        return res
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Database error: {ex}")


@router_product.patch("/", response_model=ProductAggregationResponse)
async def aggregate(item: ProductAggregationRequest,
                    async_session: AsyncSession = Depends(get_async_session)):

    """"Эндпойнт "аггрегации" продукции"""""

    try:
        res = await db_products._aggregate_date(item=item,
                                                async_session=async_session)
        return res
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Database error: {ex}")
