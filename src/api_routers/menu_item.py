from fastapi import APIRouter, HTTPException, status

from src.database import db_dep
from src.models import MenuItem, FoodPlace
from src.schemas.menu_item import CreateMenuItemSchema, MenuItemSchema
from src.security import actual_user_id_dep, only_admin_dep

router = APIRouter(prefix="/menu_items", tags=["MenuItem"])


@router.get("/{item_id}")
async def get_menu_item(item_id: int, session: db_dep, user_id: actual_user_id_dep) -> MenuItemSchema:
    menu_item = await session.get(MenuItem, item_id)
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    return MenuItemSchema.model_validate(menu_item)
    

@router.post("")
async def create_menu_item(menu_item_schema: CreateMenuItemSchema, session: db_dep,
                           user_id: only_admin_dep) -> MenuItemSchema:
    place = await session.get(FoodPlace, menu_item_schema.food_place_id)
    if not place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food place not found")
    menu_item = MenuItem(**menu_item_schema.model_dump())
    session.add(menu_item)
    await session.commit()
    await session.refresh(menu_item)
    return MenuItemSchema.model_validate(menu_item)


@router.delete("/{item_id}")
async def delete_menu_item(item_id: int, session: db_dep, user_id: only_admin_dep):
    menu_item = await session.get(MenuItem, item_id)
    if not menu_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")
    session.delete(menu_item)
    await session.commit()
    return {"detail": "Menu item deleted"}
