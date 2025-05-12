from fastapi import APIRouter

from src.api_routers import auth, user, reservation, food_table, food_place, location

api_router = APIRouter(prefix="/api")
api_router.include_router(auth.router)
api_router.include_router(user.router)

api_router.include_router(location.router)
api_router.include_router(food_place.router)
api_router.include_router(food_table.router)
api_router.include_router(reservation.router)


