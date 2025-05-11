from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import db_dep
from src.security import actual_user_id_dep, only_authenticated_dep
from src.models import FoodPlace, Location
from src.schemas.food_place import FoodPlaceSchema, CreateFoodPlaceSchema, UpdateFoodPlaceSchema

router = APIRouter(prefix="/food_places", tags=["FoodPlaces"])


@router.get("")
async def list_food_places(session: db_dep):
    request = select(FoodPlace)
    response = await session.execute(request)
    food_places = [FoodPlaceSchema.model_validate(food_place) for food_place in response.scalars().all()]
    return food_places


@router.get("/{food_place_id}")
async def retrieve_food_place(food_place_id: int, session: db_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return FoodPlaceSchema.model_validate(food_place)


@router.post("")
async def create_food_place(food_place_schema: CreateFoodPlaceSchema, session: db_dep,
                            is_authenticated: only_authenticated_dep):
    location = session.get(Location, food_place_schema.location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location with this id not found")
    check_request = select(FoodPlace).where(
        FoodPlace.name == food_place_schema.name and FoodPlace.location_id == food_place_schema.location_id)
    if (await session.execute(check_request)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="FoodPlace with this name and location_id already exists")
    food_place = FoodPlace(**food_place_schema.model_dump())
    session.add(food_place)
    await session.commit()
    await session.refresh(food_place)
    return FoodPlaceSchema.model_validate(food_place)


@router.patch("/{food_place_id}")
async def update_food_place(food_place_id: int, food_place_schema: UpdateFoodPlaceSchema, session: db_dep,
                            is_authenticated: only_authenticated_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodPlace not found")
    check_request = select(FoodPlace).where(
        FoodPlace.name == food_place_schema.name and FoodPlace.location_id == food_place.location_id)
    if (await session.execute(check_request)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="FoodPlace with this name and location_id already exists")
    for attr, value in food_place_schema.model_dump().items():
        setattr(food_place, attr, value)
    await session.commit()
    await session.refresh(food_place)
    return FoodPlaceSchema.model_validate(food_place)


@router.delete("/{food_place_id}")
async def destroy_food_place(food_place_id: int, session: db_dep, is_authenticated: only_authenticated_dep):
    food_place = await session.get(FoodPlace, food_place_id)
    if food_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodPlace not found")
    await session.delete(food_place)
    await session.commit()
    return {"detail": "FoodPlace deleted"}
