from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.config import BaseSchema
from src.database import db_dep
from src.models import MenuItem, FoodBasket
from src.schemas.basket_item import CreateBasketItemSchema, BasketItemSchema
from src.schemas.food_basket import FoodBasketSchema
from src.schemas.menu_item import CreateMenuItemSchema, MenuItemSchema
from src.security import actual_user_id_dep

router = APIRouter(prefix="/food_baskets", tags=["FoodBasket"])


class IdMenuItemSchema(BaseSchema):
    id: int


@router.post("/{basket_id}")
async def create_basket_item(menu_item_schema: IdMenuItemSchema, basket_id: int, session: db_dep,
                             user_id: actual_user_id_dep):
    menu_item = await session.get(MenuItem, menu_item_schema.id)
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    menu_item_schema = MenuItemSchema.model_validate(menu_item)
    food_basket = await session.scalar(select(FoodBasket).where(FoodBasket.user_id == user_id))
    if not food_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food basket not found")
    basket_item_schema = CreateMenuItemSchema(food_basket_id=food_basket.id,
                                              menu_item_id=menu_item_schema.id)
    basket_item = CreateBasketItemSchema(**basket_item_schema.model_dump())
    session.add(basket_item)
    session.commit()
    session.refresh(basket_item)
    return BasketItemSchema.model_validate(basket_item)


@router.get("")
async def list_baskets(session: db_dep, user_id: actual_user_id_dep):
    food_stmt = select(FoodBasket).where(FoodBasket.user_id == user_id)
    food_baskets = await session.scalars(food_stmt)
    return [FoodBasketSchema.model_validate(food_basket) for food_basket in food_baskets]


# @router.get("/active")
async def get_active_basket_with_menu_items(session: db_dep, user_id: actual_user_id_dep):
    food_basket = await session.scalar(
        select(FoodBasket).where(FoodBasket.user_id == user_id, FoodBasket.is_ordered is False))
    if not food_basket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pass
