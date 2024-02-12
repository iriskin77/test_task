from datetime import datetime
from task.models import Task, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from product.schema import ProductAddTasks, ProductAggregation, ProductBase
from fastapi import HTTPException


async def _product_create(items: ProductAddTasks,
                          async_session: AsyncSession):

    products_to_add = []
    for new_product in items.dict()['products']:

        task = await get_task_by_num_date_batch(number_batch_id=new_product['number_batch_id'],
                                                date_product=new_product['date_product'],
                                                async_session=async_session)

        product = await get_product_by_unique_code(unique_code=new_product['unique_code'],
                                                   async_session=async_session)

        # Если продукция передана с несуществующей партией (нет сменного задания с указаным номером партии и датой партии), то данную продукцию можно игнорировать.
        if task is None:
            #  Если переданная продукция с данным уникальным кодом уже существует, то ее можно игнорировать.
            if product is None:
                new_product_to_add = {
                            "unique_code": new_product['unique_code'],
                            "number_batch_id": new_product['number_batch_id'],
                            "date_product": new_product['date_product']
                            }

                dict_product = Product(**new_product)
                products_to_add.append(ProductBase(**new_product))
                async_session.add(dict_product)

    if products_to_add == []:
        raise HTTPException(status_code=404, detail="No products to add")

    await async_session.commit()

    return {'products': products_to_add}


async def get_task_by_num_date_batch(number_batch_id,
                                     date_product,
                                     async_session: AsyncSession):
    query_task = select(Task).\
            where(and_(Task.number_batch == number_batch_id,
                       Task.date_batch == date_product))

    task = await async_session.execute(query_task)
    task_row = task.fetchone()
    if task_row is not None:
        return task_row[0]


async def get_product_by_unique_code(unique_code,
                                     async_session: AsyncSession):

    query_product = select(Product).where(Product.unique_code == unique_code)
    product = await async_session.execute(query_product)
    product_row = product.fetchone()
    if product_row is not None:
        return product_row[0]


# ================ Aggregation data ================

async def _aggregate_date(item: ProductAggregation,
                          async_session: AsyncSession):

    product = await get_product_by_unique_code(unique_code=item.unique_code,
                                               async_session=async_session)

    if product is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if product.is_aggregated:
        raise HTTPException(status_code=400,
                            detail=f"unique code already used at {product.is_aggregated}")

    query_task = select(Task).where(Task.id == item.task_id)
    task = await async_session.execute(query_task)
    task_check = task.fetchone()[0]
    if task_check is None:
        raise HTTPException(status_code=404, detail="Not Found")

    if task_check.number_batch != product.number_batch_id:
        raise HTTPException(status_code=400,
                            detail="unique code is attached to another batch")

    product.is_aggregated = True
    product.aggregated_at = datetime.now()

    await async_session.commit()
    return product

