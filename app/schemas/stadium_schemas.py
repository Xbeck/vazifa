from datetime import date, datetime, time
from pydantic import BaseModel, Field

from app.schemas.examples import ExampleStadium, ExampleBooking
from app.utils.enums import BookingStatus


class BaseStadiumSchema(BaseModel):
    """Base for the Stadium Schema."""

    name: str = Field(examples=[ExampleStadium.name])
    address: str = Field(examples=[ExampleStadium.address])
    contact: str = Field(examples=[ExampleStadium.contact])
    images: list[str] = Field(examples=[ExampleStadium.images])
    price_per_hour: int = Field(examples=[ExampleStadium.price_per_hour])
    latitude: float = Field(examples=[ExampleStadium.latitude])
    longitude: float = Field(examples=[ExampleStadium.longitude])
    description: str = Field(examples=[ExampleStadium.description])


class StadiumRequestSchema(BaseStadiumSchema):
    """Request schema for creating a Stadium."""
    pass


class StadiumResponseSchema(BaseStadiumSchema):
    """Response Schema for a Stadium."""

    id: int = Field(examples=[ExampleStadium.id])
    owner_id: int = Field(examples=[ExampleStadium.owner_id])





class BaseBookingSchema(BaseModel):
    """Base for the Booking Schema."""

    date_at: date = Field(examples=[ExampleBooking.date_at])
    start_time: time = Field(examples=[ExampleBooking.start_time])
    end_time: time = Field(examples=[ExampleBooking.end_time])


class BookingRequestSchema(BaseBookingSchema):
    """Request schema for creating a Booking."""
    pass


class BookingResponseSchema(BaseBookingSchema):
    """Response Schema for a Booking."""

    id: int = Field(examples=[ExampleBooking.id])
    user_id: int = Field(examples=[ExampleBooking.user_id])
    stadium_id: int = Field(examples=[ExampleBooking.stadium_id])
    status: BookingStatus = Field(examples=[ExampleBooking.status])
    created_at: datetime = Field(examples=[ExampleBooking.created_at])


