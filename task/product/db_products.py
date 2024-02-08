from datetime import datetime
from task.models import Task, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from task.product.schema import ProductAddTasks, ProductAggregation
from fastapi import HTTPException


async def _product_create(items: ProductAddTasks, async_session: AsyncSession):

    for product in items.dict()['products']:

        query_task = select(Task).\
            where(and_(Task.number_batch == product['number_batch_id'],
                       Task.date_batch == product['date_product']))
        query_unique_code = select(Product).filter(Product.unique_code == product['unique_code'])
        task = await async_session.execute(query_task)
        unique_code = await async_session.execute(query_unique_code)

        if task is not None:
            if unique_code is not None:

                new_product = Product(unique_code=product['unique_code'],
                                      number_batch_id=product['number_batch_id'],
                                      date_product=product['date_product'])
                async_session.add(new_product)
    await async_session.commit()


async def _aggregate_date(item: ProductAggregation, async_session: AsyncSession):

    query_product = select(Product).where(Product.unique_code == item.unique_code)
    product = await async_session.execute(query_product)
    product_to_update = product.fetchone()

    if product_to_update is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if product_to_update[0].is_aggregated:
        raise HTTPException(status_code=400, detail=f"unique code already used at {product.fetchone()[0].is_aggregated}")

    query_task = select(Task).where(Task.id == item.task_id)
    task = await async_session.execute(query_task)
    task_check = task.fetchone()[0]
    if task_check is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if task_check.number_batch != product_to_update[0].number_batch_id:
        raise HTTPException(status_code=400, detail="unique code is attached to another batch")

    product_to_update[0].is_aggregated = True
    product_to_update[0].aggregated_at = datetime.now()

    await async_session.commit()
