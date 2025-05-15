from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import CheckConstraint, String
from typing import TYPE_CHECKING

from src.database import Base

if TYPE_CHECKING:
    from src.models import Reservation


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    reservations: Mapped[list["Reservation"]] = relationship("Reservation", back_populates="user")
