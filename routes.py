from fastapi import APIRouter
from task import task_handlers


routes = APIRouter()


routes.include_router(router=task_handlers.router_task, prefix="/task")
