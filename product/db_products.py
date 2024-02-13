from datetime import datetime
from task.models import Task, Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from product.schema import ListAddProducts, ProductAggregationRequest, ProductBase
from fastapi import HTTPException
from task.db_tasks import _get_task_by_id


async def _product_create(items: ListAddProducts,
                          async_session: AsyncSession):

    products_to_add = []
    for new_product in items.products:

        task = await get_task_by_num_date_batch(number_batch_id=new_product.number_batch_id,
                                                date_product=new_product.date_product,
                                                async_session=async_session)

        product = await get_product_by_unique_code(unique_code=new_product.unique_code,
                                                   async_session=async_session)

        # Если продукция передана с несуществующей партией (== None),
        # т.е. нет сменного задания с указаным номером партии и датой партии, то данную продукцию можно игнорировать.
        if task is not None:
            #  Если переданная продукция с данным уникальным кодом уже существует, то ее можно игнорировать.
            if product is None:

                dict_product = Product(**new_product.dict())
                products_to_add.append(new_product)

                async_session.add(dict_product)

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

async def _aggregate_date(item: ProductAggregationRequest,
                          async_session: AsyncSession):

    product = await get_product_by_unique_code(unique_code=item.unique_code,
                                               async_session=async_session)

    # Если продукции с данным уникальным кодом не существует, то необходимо вернуть 404 ошибку.
    if product is None:
        raise HTTPException(status_code=404, detail="Not Found")

    # Если данный уникальный код уже был использован, то вернуть 400 ошибку
    if product.is_aggregated:
        raise HTTPException(status_code=400,
                            detail=f"unique code already used at {product.is_aggregated}")

    task = await _get_task_by_id(id=item.task_id, async_session=async_session)
    if task is None:
        raise HTTPException(status_code=404, detail="Task with this id was not found")

    # Если уникальный код существует, но привязан к другой партии, необходимо вернуть 400 ошибку
    if task.number_batch != product.number_batch_id:
        raise HTTPException(status_code=400,
                            detail="unique code is attached to another batch")

    product.is_aggregated = True
    product.aggregated_at = datetime.now()
    print(product.unique_code)

    await async_session.commit()
    return item

