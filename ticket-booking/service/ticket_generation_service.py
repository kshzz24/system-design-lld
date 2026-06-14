from entities.booking import Booking
from entities.ticket import Ticket
import uuid
from datetime import datetime
from enums.enums import BookingStatus


class TicketGenerationService:

    def __init__(self) -> None:
        self._tickets: dict[str, Ticket] = {}

    def generate_ticket(self, booking: Booking) -> Ticket:
        ticket_id = str(uuid.uuid4())

        if booking.status != BookingStatus.CONFIRMED:
            raise ValueError("Cannot generate ticket for a non-confirmed booking")

        ticket = Ticket(
            ticket_id=ticket_id, booking=booking, generated_at=datetime.now()
        )
        self._tickets[ticket.ticket_id] = ticket
        return ticket

    def print_ticket(self, ticket_id: str) -> str:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} not found")
        return f"Ticket = {ticket}"
