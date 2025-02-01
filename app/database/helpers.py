from typing import Any, Optional
from sqlalchemy import select
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Booking, Stadium, User


class UserDB:

    @staticmethod
    async def all(session: AsyncSession) -> Sequence[User]:
        """Return all Users in the database."""
        result = await session.execute(select(User))
        return result.scalars().all()

    @staticmethod
    async def get(session: AsyncSession, user_id: int = None, email: str = None) -> Optional[User]:
        if user_id:
            """Return a specific user by their email address."""
            result = await session.execute(select(User).where(User.id == user_id))
            return result.scalars().first()

        elif email:
            """Return a specific user by their email address."""
            result = await session.execute(select(User).where(User.email == email))
            return result.scalars().first()

        else:
            raise ValueError("Provide user_id or email to get related user.")

    @staticmethod
    async def create(session: AsyncSession, user_data: dict[str, Any]) -> User:
        """Add a new user to the database."""
        new_user = User(**user_data)
        session.add(new_user)
        return new_user




class StadiumDB:

    @staticmethod
    async def all(session: AsyncSession) -> Sequence[Stadium]:
        """Return all stadiums in the database."""
        result = await session.execute(select(Stadium))
        return result.scalars().all()

    @staticmethod
    async def get(session: AsyncSession, stadium_id: int) -> Optional[Stadium]:
        """Return an stadium by its id"""
        result = await session.execute(select(Stadium).where(Stadium.id == stadium_id))
        return result.scalars().first()




class BookingDB:

    @staticmethod
    async def all(session: AsyncSession) -> Sequence[Booking]:
        """Return all booking in the database."""
        result = await session.execute(select(Booking))
        return result.scalars().all()

    @staticmethod
    async def get(session: AsyncSession, booking_id: int) -> Optional[Booking]:
        """Return an booking by its id"""
        result = await session.execute(select(Booking).where(Booking.id == booking_id))
        return result.scalars().first()