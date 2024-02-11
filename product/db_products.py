from datetime import datetime
from task.models import Task, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from product.schema import ProductAddTasks, ProductAggregation, ProductBase
from fastapi import HTTPException


async def _product_create(items: ProductAddTasks, async_session: AsyncSession):
    products_to_add = []
    for product in items.dict()['products']:

        query_task = select(Task).\
            where(and_(Task.number_batch == product['number_batch_id'],
                       Task.date_batch == product['date_product']))
        query_unique_code = select(Product).filter(Product.unique_code == product['unique_code'])
        task = await async_session.execute(query_task)
        unique_code = await async_session.execute(query_unique_code)

        if task is not None:
            if unique_code is not None:

                new_product_to_add = {"id": product['id'],
                                      "unique_code": product['unique_code'],
                                      "number_batch_id": product['number_batch_id'],
                                      "date_product": product['date_product']}
                dict_product = Product(**new_product_to_add)
                products_to_add.append(ProductBase(**new_product_to_add))

                async_session.add(dict_product)
    await async_session.commit()

    return {'products': products_to_add}


async def _aggregate_date(item: ProductAggregation, async_session: AsyncSession):

    product = await get_product_by_unique_code(item=item, async_session=async_session)

    if product is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if product.is_aggregated:
        raise HTTPException(status_code=400, detail=f"unique code already used at {product.is_aggregated}")

    query_task = select(Task).where(Task.id == item.task_id)
    task = await async_session.execute(query_task)
    task_check = task.fetchone()[0]
    if task_check is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if task_check.number_batch != product.number_batch_id:
        raise HTTPException(status_code=400, detail="unique code is attached to another batch")

    product.is_aggregated = True
    product.aggregated_at = datetime.now()

    await async_session.commit()
    return product


async def get_product_by_unique_code(item: ProductAggregation, async_session: AsyncSession):
    query_product = select(Product).where(Product.unique_code == item.unique_code)
    product = await async_session.execute(query_product)
    product_row = product.fetchone()
    if product_row is not None:
        return product_row[0]
