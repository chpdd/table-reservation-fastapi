from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
import datetime as dt

from typing import TYPE_CHECKING

from src.database import Base

while TYPE_CHECKING:
    from src.models import FoodPlace, User


class Reservation(Base):
    __tablename__ = "food_tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    start_time: Mapped[dt.datetime] = mapped_column()
    end_time: Mapped[dt.datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    food_table_id: Mapped[int] = mapped_column(ForeignKey("food_tables.id", ondelete="CASCADE"))

    user: Mapped["User"] = relationship("User", back_populates="reservations")
    food_table: Mapped["FoodPlace"] = relationship("FoodTable", back_populates="reservations")
