from enums.enums import SeatType, SeatStatus
from datetime import datetime
from entities.user import User
from dataclasses import dataclass
from typing import Optional


@dataclass
class Seat:
    seat_id: str
    seat_type: SeatType
    seat_number: str
    cost: float
    status: SeatStatus = SeatStatus.AVAILABLE
    locked_by: Optional[User] = None
    locked_at: Optional[datetime] = None
