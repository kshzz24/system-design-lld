from dataclasses import dataclass
from entities.booking import Booking
from datetime import datetime


@dataclass
class Ticket:
    ticket_id: str
    booking: Booking
    generated_at: datetime
    