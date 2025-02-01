"""Define the Users model."""

from datetime import date, datetime, time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ARRAY, Boolean,
    Date, DateTime,
    Enum, Float, ForeignKey,
    Integer, Numeric,
    String, Text,
    Time, 
    )

from app.database.db import Base
from app.utils.enums import BookingStatus, PaymentMethod, PaymentStatus, RoleType




class User(Base):
    """Define the Users model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(50))
    role: Mapped[RoleType] = mapped_column(
        Enum(RoleType),
        nullable=False,
        server_default=RoleType.user.name,
        index=True,
    )
    banned: Mapped[bool] = mapped_column(Boolean, default=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    stadiums: Mapped[list["Stadium"]] = relationship(back_populates="owner")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'User({self.id}, "{self.first_name} {self.last_name}")'


class Stadium(Base):
    """Define the Stadium model."""

    __tablename__ = "stadiums"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    contact: Mapped[str] = mapped_column(String(13))
    images: Mapped[list[str]] = mapped_column(ARRAY(String))
    price_per_hour: Mapped[int] = mapped_column(Numeric())
    
    # location: Mapped[list[float]] = mapped_column(ARRAY(Float), index=True) # (lat, long)
    latitude: Mapped[float]= mapped_column(Float, index=True)
    longitude: Mapped[float]= mapped_column(Float, index=True)

    description: Mapped[str] = mapped_column(Text)

    # Relationship
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["User"] = relationship("User", back_populates="stadiums")

    bookings: Mapped["Booking"] = relationship(back_populates="stadium")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Stadium({self.id}, "{self.name}")'


class Booking(Base):
    """Define the Booking model."""

    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    date_at: Mapped[date] = mapped_column(Date, index=True)
    start_time: Mapped[time] = mapped_column(Time, index=True)
    end_time: Mapped[time] = mapped_column(Time, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus),
        nullable=False,
        server_default=BookingStatus.not_started.value,
        index=True
    )

    # Relationship
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="bookings")

    stadium_id: Mapped[int] = mapped_column(ForeignKey("stadiums.id"))
    stadium: Mapped["Stadium"] = relationship("Stadium", back_populates="bookings")

    payment: Mapped[list["Payment"]] = relationship(back_populates="booking")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Booking({self.id})'



class Payment(Base):
    """Define the Payment model."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[int] = mapped_column(Integer())
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    payment_method: Mapped[PaymentMethod] = mapped_column(
        Enum(PaymentMethod),
        nullable=False,
        server_default=PaymentMethod.cash.value
    )

    card_number: Mapped[str] = mapped_column(String(length=16), nullable=True)
    exp_date: Mapped[str] = mapped_column(String(length=5), nullable=True)

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        nullable=False,
        server_default=PaymentStatus.pending.value,
        index=True
    )

    # Relationship
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    booking: Mapped["Booking"] = relationship("Booking", back_populates="payment")

    def __repr__(self) -> str:
        """Define the model representation."""
        return f'Payment({self.id})'


