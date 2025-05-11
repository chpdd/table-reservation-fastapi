from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import db_dep
from src.security import actual_user_id_dep, only_admin_dep
from src.models import Reservation, FoodTable
from src.schemas.reservation import ReservationSchema, CreateReservationSchema, UpdateReservationSchema

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("")
async def list_reservations(session: db_dep, user_id: actual_user_id_dep):
    request = select(Reservation).where(Reservation.user_id == user_id)
    response = await session.execute(request)
    reservations = [ReservationSchema.model_validate(reservation) for reservation in response.scalars().all()]
    return reservations


@router.route('/all')
async def list_all_reservations(session: db_dep, user_id: only_admin_dep):
    request = select(Reservation)
    response = await session.execute(request)
    reservations = [ReservationSchema.model_validate(reservation) for reservation in response.scalars().all()]
    return reservations


@router.get("/{reservation_id}")
async def retrieve_reservation(reservation_id: int, session: db_dep, user_id: actual_user_id_dep):
    reservation = await session.get(Reservation, reservation_id)
    if reservation is None or reservation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return ReservationSchema.model_validate(reservation)


@router.post("")
async def create_reservation(reservation_schema: CreateReservationSchema, session: db_dep,
                             user_id: actual_user_id_dep):
    food_table = session.get(FoodTable, reservation_schema.food_table_id)
    if food_table is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="FoodTable with this id not found")
    # Добавить проверку занятости на данное время
    reservation = Reservation(**reservation_schema.model_dump(), user_id=user_id)
    session.add(reservation)
    await session.commit()
    await session.refresh(reservation)
    return ReservationSchema.model_validate(reservation)


@router.put("/{reservation_id}")
async def update_reservation(reservation_id: int, reservation_schema: UpdateReservationSchema, session: db_dep,
                             user_id: actual_user_id_dep):
    reservation = await session.get(Reservation, reservation_id)
    if reservation is None or reservation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    # Добавить проверку занятости на новое время
    for attr, value in reservation_schema.model_dump().items():
        setattr(reservation, attr, value)
    await session.commit()
    await session.refresh(reservation)
    return ReservationSchema.model_validate(reservation)


@router.delete("/{reservation_id}")
async def destroy_reservation(reservation_id: int, session: db_dep, user_id: actual_user_id_dep):
    reservation = await session.get(Reservation, reservation_id)
    if reservation is None or reservation.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    await session.delete(reservation)
    await session.commit()
    return {"detail": "Reservation deleted"}
