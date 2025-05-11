from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from typing import TYPE_CHECKING

from src.database import Base

while TYPE_CHECKING:
    from src.models import Location


class FoodPlace(Base):
    __tablename__ = "places"
    __table_args__ = (
        UniqueConstraint("name", "location_id", name="unique_name_per_location_id")
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"))

    location: Mapped["Location"] = relationship("Location", back_populates="food_places")



