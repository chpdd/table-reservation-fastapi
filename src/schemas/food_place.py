import datetime as dt
from pydantic import field_validator

from src.config import BaseSchema


class CreateFoodPlaceSchema(BaseSchema):
    name: str
    address: str
    description: str
    open_time: dt.time
    close_time: dt.time
    location_id: int

    @field_validator("open_time", "close_time", mode="before")
    def parse_time(cls, v):
        if isinstance(v, str):
            try:
                return dt.datetime.strptime(v, "%H:%M").time()
            except ValueError:
                raise ValueError("Time should be of the form Hours:minutes")
        return v


class UpdateFoodPlaceSchema(BaseSchema):
    name: str | None
    address: str | None
    description: str | None
    open_time: dt.time | None
    close_time: dt.time | None
    location_id: int | None

    # @field_validator("open_time", "close_time", mode="before")
    # def parse_time(cls, v):
    #     if isinstance(v, str):
    #         try:
    #             return dt.datetime.strptime(v, "%H:%M").time()
    #         except ValueError:
    #             raise ValueError("Time should be of the form Hours:minutes")
    #     return v


class FoodPlaceSchema(CreateFoodPlaceSchema):
    id: int
