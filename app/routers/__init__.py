from fastapi import APIRouter
from . import auth, stadium_router, user_router

routers = APIRouter()

routers.include_router(auth.router)
routers.include_router(user_router.router)
routers.include_router(stadium_router.router)
