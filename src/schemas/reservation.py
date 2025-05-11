import datetime as dt

from src.config import BaseSchema


class CreateReservationSchema(BaseSchema):
    start_date: dt.datetime
    end_date: dt.datetime
    food_table_id: int


class UpdateReservationSchema(BaseSchema):
    start_date: dt.datetime | None
    end_date: dt.datetime | None
    food_table_id: int | None
    is_active: bool | None


class ReservationSchema(UpdateReservationSchema):
    id: int
    user_id: int
