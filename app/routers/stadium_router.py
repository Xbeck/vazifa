from collections.abc import Sequence
from datetime import date, time
from typing import Optional, Union
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_database
from app.managers.auth import is_owner, oauth2_schema
from app.managers.stadium_manager import BookingManager, StadiumManager
from app.models import Booking, Stadium
from app.schemas.stadium_schemas import BookingRequestSchema, BookingResponseSchema, StadiumRequestSchema, StadiumResponseSchema


router = APIRouter(tags=["Stadiums"], prefix="/stadiums")



# 2.Maydon egalari
#     -Futbol maydonni kiritish, tahrirlash
#      (nomi, address, contact, rasmlari, 1soatlik bron qilish narxi, va hokazo). 
#     -Bronlarni ko'rish
#     -Bronni o'chirish

@router.post("/add",
            dependencies=[Depends(oauth2_schema), Depends(is_owner)],
            response_model=StadiumResponseSchema,
            status_code=201)
async def add_stadium(
    request: Request,
    stadium_data: StadiumRequestSchema,
    db: AsyncSession = Depends(get_database)) -> Stadium:
    """
    Create an stadium

    This route is only allowed for Admin or Owner.
    """
    stadium = await StadiumManager.create_stadium(stadium_data, request.state.user.id, db)
    return stadium


@router.put("/{stadium_id}/update",
            dependencies=[Depends(oauth2_schema), Depends(is_owner)],
            response_model=StadiumResponseSchema,
            status_code=200)
async def update_stadium(
    request: Request,
    stadium_id: int,
    new_data: StadiumRequestSchema,
    db: AsyncSession = Depends(get_database)
) -> StadiumResponseSchema:
    """Update the specified Stadium's data. | Available for the specific requesting Owner, or an Admin."""
    owner_id = request.state.user.id
    await StadiumManager.update_stadium(stadium_id, owner_id, new_data, db)
    return await StadiumManager.get_stadium_by_id(stadium_id, db)


@router.get("/{stadium_id}/bookings",
            dependencies=[Depends(oauth2_schema), Depends(is_owner)],
            response_model=Union[BookingResponseSchema, list[BookingResponseSchema], None],
            status_code=200)
async def get_bookings(
    request: Request,
    stadium_id: int,
    booking_id: Optional[int] = None,
    db: AsyncSession = Depends(get_database)
) -> Union[Sequence[Booking], Booking]:
    """
    Get all bookings in the stadium's or a specific booking by their ID.

    stadium_id is required.

    booking_id is optional, and if omitted then all Bookings are returned.

    This route is only allowed for Admins or Owners.
    """
    owner_id = request.state.user.id
    if booking_id:
        return await StadiumManager.get_stadium_bookings(stadium_id, owner_id, db, booking_id)
    return await StadiumManager.get_stadium_bookings(stadium_id, owner_id, db)


@router.delete("/{stadium_id}/bookings/{booking_id}/delete",
                dependencies=[Depends(oauth2_schema), Depends(is_owner)],
                status_code=status.HTTP_204_NO_CONTENT
)
async def delete_booking(
    request: Request,
    stadium_id: int,
    booking_id: int,
    db: AsyncSession = Depends(get_database)
) -> None:
    """Delete the specified Booking by booking_id | Owner only."""
    owner_id = request.state.user.id
    await StadiumManager.delete_stadium_booking_by_id(stadium_id, owner_id, booking_id, db)





# 3.User
#     -Maydonlar ro'yhatini ko'rish.
#         Bunda ma'lum vaqt bilan filter qilish imkoni bo'lishi kerak,
#         yani kiritilgan vaqt oralig'idagi bron qilinmagan maydonlar ko'rsatiladi.
#         Turgan lokatsiyasi bo'yicha eng yaqin maydonlarni chiqarish bo'yicha sort ham bo'lishi kerak.
#         Hammasi bitta endpointda bo'ladi.
#     -Maydon haqida to'liq malumotni ko'rish
#     -Maydonni bron qilish

@router.get("/",
            response_model=list[StadiumResponseSchema],
            status_code=200
            )
async def get_stadiums_by_filter(
    selected_date: date,
    start_time: time,
    end_time: time,
    latitude: float, # sorted
    longitude: float,
    db: AsyncSession = Depends(get_database)
) -> Sequence[Stadium]:
    """Get all stadiums."""
    return await StadiumManager.get_stadiums_by_filter(
        selected_date,
        start_time,
        end_time,
        latitude,
        longitude,
        db
    )


@router.get("/{stadium_id}",
            response_model=StadiumResponseSchema,
            status_code=200
            )
async def get_stadium_by_id(stadium_id: int, db: AsyncSession = Depends(get_database)) -> Stadium:
    """Get a stadium by their ID"""
    return await StadiumManager.get_stadium_by_id(stadium_id, db)


@router.post("/{stadium_id}/bookings/create",
             dependencies=[Depends(oauth2_schema)],
             response_model=BookingRequestSchema)
async def create_stadium_booking(
    request: Request,
    stadium_id: int,
    booking_data: BookingRequestSchema,
    db: AsyncSession = Depends(get_database)
) -> BookingResponseSchema:
    """Create a stadium booking"""
    user_id = request.state.user.id
    return await BookingManager.create_booking(user_id,
                                               stadium_id,
                                               booking_data,
                                               db
                                            )

