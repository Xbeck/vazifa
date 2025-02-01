from datetime import date, datetime, time
from collections.abc import Sequence

from fastapi import HTTPException, status
from sqlalchemy import and_, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.helpers import BookingDB, StadiumDB
from app.models import Booking, Stadium
from app.schemas.stadium_schemas import BookingRequestSchema, BookingResponseSchema, StadiumRequestSchema, StadiumResponseSchema



class ErrorStadiumMessages:
    """Define text error responses."""

    STADIUM_EXISTS = "A Stadium with this name already exists"
    STADIUM_INVALID = "Stadium does not exist"




class StadiumManager:
    """Class to Manage the Stadium."""

    @staticmethod
    async def create_stadium(
        stadium_data: StadiumResponseSchema,
        owner_id: int,
        session: AsyncSession
    ) -> StadiumResponseSchema:

        """Create a new stadium."""
        response = await session.execute(select(Stadium).where(Stadium.name == stadium_data.name))
        exists_stadium = response.scalar_one_or_none()

        if exists_stadium is not None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, ErrorStadiumMessages.STADIUM_EXISTS)

        try:
            new_stadium_data = stadium_data.model_dump()
            new_stadium_data["owner_id"] = owner_id

            stadium = Stadium(**new_stadium_data)
            session.add(stadium)

            await session.flush()
            await session.refresh(stadium)
            return stadium

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"Serverda qandaydir xatolik yuz berdi: {err}") from err

    @staticmethod
    async def get_all_stadiums(session: AsyncSession) -> Sequence[Stadium]:
        """Get all stadium"""

        try:
            stadiums = await StadiumDB.all(session)
            return stadiums

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"Stadionlar datasini olishda qandaydir xatolik yuz berdi: {err}")

    @staticmethod
    async def update_stadium(
        stadium_id: int,
        owner_id: int,
        stadium_data: StadiumRequestSchema,
        session: AsyncSession) -> None:
        """Update the Stadium with specified ID."""
        check_stadium = await StadiumDB.get(session, stadium_id=stadium_id)
        if not check_stadium:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {stadium_id}) stadion topilmadi.")

        if owner_id != check_stadium.owner_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Bunday amalni bajarish uchun ruxsat yo'q!")

        await session.execute(
            update(Stadium).where(Stadium.id == stadium_id).values(
                name=stadium_data.name,
                address=stadium_data.address,
                contact=stadium_data.contact,
                images=stadium_data.images,
                latitude=stadium_data.latitude,
                longitude=stadium_data.longitude,
                price_per_hour=stadium_data.price_per_hour,
                description=stadium_data.description,
            )
        )

    @staticmethod
    async def delete_stadium(stadium_id: int, owner_id: int, session: AsyncSession) -> None:
        """Delete the Stadium with specified ID."""
        check_stadium = await StadiumDB.get(session, stadium_id=stadium_id)
        if not check_stadium:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {stadium_id}) stadion topilmadi")

        if owner_id != check_stadium.owner_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Bunday amalni bajarish uchun ruxsat yo'q!")

        await session.execute(delete(Stadium).where(Stadium.id == stadium_id))

    @staticmethod
    async def get_stadium_bookings(
        stadium_id: int,
        owner_id: int,
        session: AsyncSession,
        booking_id: int = None) -> Sequence[Booking]:
        """
        Get all bookings in the stadium's or a specific booking by their ID.

        stadium_id is required.

        booking_id is optional, and if omitted then all Bookings are returned.
        """

        check_stadium = await StadiumDB.get(session, stadium_id)
        if check_stadium is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {stadium_id} li) stadion topilmadi")

        if owner_id != check_stadium.owner_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Bunday amalni bajarish uchun ruxsat yo'q!")
        
        if booking_id:
            booking = await BookingDB.get(session, booking_id)
            if booking is None:
                raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {booking_id} li) bron topilmadi")
            return booking
    
        try:
            bookings = await BookingDB.all(session)
            return bookings

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"Stadion lar datasini olishda qandaydir xatolik yuz berdi: {err}")

    @staticmethod
    async def delete_stadium_booking_by_id(stadium_id: int, owner_id: int, booking_id: int, session: AsyncSession) -> None:
        """Delete the Booking with specified ID."""
        check_stadium = await StadiumDB.get(session, stadium_id=stadium_id)
        if not check_stadium:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {stadium_id}) stadion topilmadi")

        if owner_id != check_stadium.owner_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f"Bunday amalni bajarish uchun ruxsat yo'q!")
        
        check_boking = await BookingDB.get(session, booking_id)
        if not check_boking:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {booking_id}) bron topilmadi")

        await session.execute(delete(Booking).where(Booking.id == booking_id))




    # 3.User
    #     -Maydonlar ro'yhatini ko'rish.
    #         Bunda ma'lum vaqt bilan filter qilish imkoni bo'lishi kerak,
    #         yani kiritilgan vaqt oralig'idagi bron qilinmagan maydonlar ko'rsatiladi.
    #         Turgan lokatsiyasi bo'yicha eng yaqin maydonlarni chiqarish bo'yicha sort ham bo'lishi kerak.
    #         Hammasi bitta endpointda bo'ladi.
    #     -Maydon haqida to'liq malumotni ko'rish
    #     -Maydonni bron qilish

    @staticmethod
    async def get_stadiums_by_filter(
        date_at: date,
        start_time: time,
        end_time: time,
        user_latitude: float,
        user_longitude: float,
        session: AsyncSession) -> Sequence[Stadium]:
        """
        Get the stadiums by filter:

        date_at: date
        start_time: time
        end_time: time
        location: lat, long: float

        return: stadions | empty list


        SELECT s.*
        FROM
            stadiums as s
        LEFT JOIN
            bookings AS b
            ON b.stadium_id = s.id
            AND b.date_at = '2025-01-25'
            AND (b.start_time <= '12:00' AND b.end_time >= '10:00')
        WHERE
            b.id IS NULL
        ORDER BY (6371 * acos(
            cos(radians(41.34448418546601)) * cos(radians(s.latitude)) *
            cos(radians(s.longitude) - radians(69.20671622603038)) +
            sin(radians(41.34448418546601)) * sin(radians(s.latitude))
        ));
        """
        if date_at < date.today():
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sa'na noto'g'ri kiritildi.")

        if date_at == date.today() and start_time < datetime.today().time() :
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Vaqt noto'g'ri kiritildi.")
        
        try:
            # user locatsiyasi 
            distance_expr = 6371 * func.acos(
                func.cos(func.radians(user_latitude)) * func.cos(func.radians(Stadium.latitude)) *
                func.cos(func.radians(Stadium.longitude) - func.radians(user_longitude)) +
                func.sin(func.radians(user_latitude)) * func.sin(func.radians(Stadium.latitude))
            ).label("distance")

            query = (
                select(Stadium, distance_expr).distinct() # dublikatlarni yo'qotadi
                .outerjoin(
                    Booking,
                    and_(
                        Booking.stadium_id == Stadium.id,
                        Booking.date_at == date_at,
                        Booking.start_time < end_time,
                        Booking.end_time > start_time
                    )
                )
                .where(Booking.id.is_(None))  # Bron qilinmaganlarini oladi
                .order_by(distance_expr) # locatsiya bo'ticha so'rt qilib oladi
            )
            result = await session.execute(query)
            return result.scalars().all()

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"Stadionlar datasini olishda qandaydir xatolik yuz berdi: {err}")

    @staticmethod
    async def get_stadium_by_id(stadium_id: int, session: AsyncSession) -> StadiumResponseSchema:
        """Get a stadium by its id"""

        stadium = await StadiumDB.get(session, stadium_id)
        if stadium is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Bunday (ID: {stadium_id}) stadion topilmadi")
        return stadium



class BookingManager:
    """Class to Manage the Booking."""

    @staticmethod
    async def create_booking(
        user_id: int,
        stadium_id: int,
        booking_data: BookingRequestSchema,
        session: AsyncSession
    ) -> BookingResponseSchema:
        """
        Create a new booking.
        
        -- stadium check for booking (kesishuv yo'q bo'lishi kerak)
        SELECT *
        FROM bookings AS b
        WHERE (
            b.stadium_id = 2 AND
            b.date_at = '2025-01-25' AND
            b.start_time < '14:00' AND b.end_time > '13:00'
        );

        -- add booking:
        INSERT INTO bookings (user_id, stadium_id, date_at, start_time, end_time)
        VALUES(1, 2, '2025-01-25', '13:00', '14:00');
        """
        existing_stadium = await session.execute(select(Stadium).where(Stadium.id == stadium_id))
        if not existing_stadium.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Stadium not found.")

        existing_booking = await session.execute(
            select(Booking).filter(
                Booking.stadium_id == stadium_id,
                Booking.date_at == booking_data.date_at,
                (Booking.start_time < booking_data.end_time) & (Booking.end_time > booking_data.start_time)
            )
        )
        if existing_booking.scalars().first():
            raise HTTPException(status_code=400, detail="Stadium already booked for this time range")

        try:
            new_booking_data = booking_data.model_dump()
            new_booking_data["user_id"] = user_id
            new_booking_data["stadium_id"] = stadium_id

            booking = Booking(**new_booking_data)
            session.add(booking)

            await session.flush()
            await session.refresh(booking)
            return booking

        except Exception as err:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR,
                                f"Serverda qandaydir xatolik yuz berdi: {err}") from err


