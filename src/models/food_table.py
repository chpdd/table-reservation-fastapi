from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from typing import TYPE_CHECKING

from src.database import Base

while TYPE_CHECKING:
    from src.models import FoodPlace


class FoodTable(Base):
    __tablename__ = "food_tables"
    __table_args__ = [
        UniqueConstraint("table_number", "food_place_id", name="unique_table_number_per_food_place_id")
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    table_number: Mapped[str] = mapped_column()
    max_seats: Mapped[int] = mapped_column()
    food_place_id: Mapped[int] = mapped_column(ForeignKey("food_places.id", ondelete="CASCADE"))

    food_place: Mapped["FoodPlace"] = relationship("FoodPlace", back_populates="food_tables")
