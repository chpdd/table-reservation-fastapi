import datetime as dt

from src.config import BaseSchema
from src.schemas.basket_item import BasketItemSchema


class FoodBasketSchema(BaseSchema):
    id: int
    ordered_at: dt.datetime | None
    is_ordered: bool


class ItemsFoodBasketSchema(FoodBasketSchema):
    items: BasketItemSchema
