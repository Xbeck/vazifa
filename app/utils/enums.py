# pylint: disable=invalid-name
"""Define Enums for this project."""

from enum import Enum


class RoleType(Enum):
    """Contains the different Role types Users can have."""

    user = "user"
    owner = "owner"
    admin = "admin"

class BookingStatus(Enum):
    """To represent the status of the Booking."""

    not_started = "not_started"
    countinuing = "countinuing"
    finished = "finished"
    canceled = "canceled"

class PaymentStatus(Enum):
    """To represent the status of the Payment."""

    pending = "pending"
    approved = "approved"
    declided = "declided"
    out_of_balance = "out_of_balance"


class PaymentMethod(Enum):
    """Contains the different Payment types Users can have."""
    
    cash = "cash"
    card = "card"