from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from src.database import db_dep
from src.models import FoodPlace, Location, MenuItem
from src.schemas.food_place import FoodPlaceSchema, CreateFoodPlaceSchema, UpdateFoodPlaceSchema
from src.schemas.menu_item import MenuItemSchema
from src.security import actual_user_id_dep, only_admin_dep

router = APIRouter(prefix="/food_places", tags=["FoodPlaces"])


@router.get("")
async def list_food_places(session: db_dep, user_id: actual_user_id_dep):
    request = select(FoodPlace)
    response = await session.execute(request)
    food_places = [FoodPlaceSchema.model_validate(food_place) for food_place in response.scalars().all()]
    return food_places


@router.get("/{food_place_id}")
async def get_food_place(food_place_id: int, session: db_dep, user_id: actual_user_id_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return FoodPlaceSchema.model_validate(food_place)


@router.post("")
async def create_food_place(food_place_schema: CreateFoodPlaceSchema, session: db_dep,
                            user_id: only_admin_dep):
    location = await session.get(Location, food_place_schema.location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location with this id not found")
    check_request = select(FoodPlace).where(
        FoodPlace.name == food_place_schema.name, FoodPlace.location_id == food_place_schema.location_id)
    if (await session.execute(check_request)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="FoodPlace with this name and location_id already exists")
    food_place = FoodPlace(**food_place_schema.model_dump())
    session.add(food_place)
    await session.commit()
    await session.refresh(food_place)
    return FoodPlaceSchema.model_validate(food_place)


@router.put("/{food_place_id}")
async def update_food_place(food_place_id: int, food_place_schema: UpdateFoodPlaceSchema, session: db_dep,
                            is_authenticated: only_admin_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodPlace not found")
    check_request = select(FoodPlace).where(
        FoodPlace.name == food_place_schema.name, FoodPlace.location_id == food_place_schema.location_id,
        FoodPlace.address == food_place_schema.address)
    if (await session.execute(check_request)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="FoodPlace with this name, location_id and address already exists")
    for attr, value in food_place_schema.model_dump().items():
        setattr(food_place, attr, value)
    await session.commit()
    await session.refresh(food_place)
    return FoodPlaceSchema.model_validate(food_place)


@router.delete("/{food_place_id}")
async def delete_food_place(food_place_id: int, session: db_dep, user_id: only_admin_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodPlace not found")
    await session.delete(food_place)
    await session.commit()
    return {"detail": "FoodPlace deleted"}


@router.get("/{food_place_id}/menu_items")
async def list_food_place_menu_items(food_place_id: int, session: db_dep, user_id: actual_user_id_dep) -> list[MenuItemSchema]:
    food_place = await session.get(FoodPlace, food_place_id)
    if not food_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodPlace not found")
    menu_items = await session.scalars(select(MenuItem).where(MenuItem.food_place_id == food_place_id))
    menu_items_schemas = [MenuItemSchema.model_validate(menu_item) for menu_item in menu_items]
    return menu_items_schemas
