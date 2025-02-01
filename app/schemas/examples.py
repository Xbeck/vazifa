"""Example data for Schemas."""


from typing import List


class ExampleUser:
    """Define a dummy user for Schema examples."""

    id = 25
    first_name = "John"
    last_name = "Doe"
    email = "user@example.com"
    password = "My S3cur3 P@ssw0rd"  # noqa: S105
    role = "user"
    banned = False
    verified = True



class ExampleStadium:
    """Define a dummy stadium for Schema examples."""

    id = 1
    owner_id = 1
    name = "Yosh kuch stadio'ni."
    address = "Toshkent sh. Olmazor tum. Beruniy ko'chasi."
    contact = "+998991234567"
    images = ["/images/img_1_1.png", "/images/img_1_2.png"]
    price_per_hour = 100
    latitude = 41.279723044819185
    longitude = 69.2126611079634
    description = "Stadion holati yaxshi, ish vaqti: 24/7"



class ExampleBooking:
    """Define a dummy booking for Schema examples."""

    id = 1
    date_at = "2025-01-25"
    start_time = "10:00"
    end_time = "12:00"
    created_at = "10:01"
    status = "not_started"
    user_id = 2
    stadium_id = 1




