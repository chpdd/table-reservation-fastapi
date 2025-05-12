from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint

from typing import TYPE_CHECKING
import datetime as dt

from src.database import Base

while TYPE_CHECKING:
    from src.models import Location, FoodTable


class FoodPlace(Base):
    __tablename__ = "food_places"
    __table_args__ = (
        UniqueConstraint("name", "location_id", name="unique_name_per_location_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    address: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    open_time: Mapped[dt.time] = mapped_column()
    close_time: Mapped[dt.time] = mapped_column()
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))

    location: Mapped["Location"] = relationship("Location", back_populates="food_places")
    food_tables: Mapped[list["FoodTable"]] = relationship("FoodTable", back_populates="food_place")