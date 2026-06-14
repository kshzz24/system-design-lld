from datetime import datetime
from entities.user import User
from entities.show import Show
from entities.seat import Seat
from enums.enums import BookingStatus
from dataclasses import dataclass, field

@dataclass
class Booking:
    booking_id: str
    user: User
    show: Show
    status: BookingStatus
    total_amount: float
    created_at: datetime
    expires_at: datetime
    seats: list[Seat] = field(default_factory=list)
