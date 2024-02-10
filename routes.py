from fastapi import APIRouter
from task import task_handlers
from product import product_handlers

routes = APIRouter()


routes.include_router(router=task_handlers.router_task, prefix="/task")
routes.include_router(router=product_handlers.router_product, prefix="/product")
