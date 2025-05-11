from src.config import BaseSchema


class CreateFoodPlaceSchema(BaseSchema):
    name: str
    address: str
    location_id: int


class UpdateFoodPlaceSchema(BaseSchema):
    name: str
    address: str


class FoodPlaceSchema(CreateFoodPlaceSchema):
    id: int
