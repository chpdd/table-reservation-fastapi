from typing import Annotated

from pydantic import Field

from src.config import BaseSchema


class CreateMenuItemSchema(BaseSchema):
    name: str
    description: Annotated[str | None, Field(default=None)]
    food_place_id: int


class MenuItemSchema(CreateMenuItemSchema):
    id: int
