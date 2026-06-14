from service.booking_service import BookingService
from service.search_service import SearchService
from service.ticket_generation_service import TicketGenerationService
from service.payment_service import PaymentService

from entities.user import User
from entities.show import Show
from entities.seat import Seat
from entities.ticket import Ticket
from payment.payment_strategy import PaymentStrategy
from typing import Optional


class TicketBookingSystem:

    def __init__(
        self,
        search_service: SearchService,
        booking_service: BookingService,
        # payment_service: PaymentService,
        ticket_generation_service: TicketGenerationService,
    ):
        self._search_service = search_service
        self._booking_service = booking_service
        self._ticket_generation_service = ticket_generation_service

    def search_movies(self, city_id: str):
        return self._search_service.select_city(city_id=city_id)

    def get_shows_for_theatre(self, theatre_id: str):
        return self._search_service.select_theatre(theatre_id=theatre_id)

    def book_tickets(
        self,
        user: User,
        show: Show,
        seats: list[Seat],
        payment_strategy: PaymentStrategy,
    ) -> Optional[Ticket]:
        try:
            created_booking = self._booking_service.create_booking(
                user=user, show=show, seats=seats
            )
            payment_service = PaymentService(strategy=payment_strategy)
            success = payment_service.process_payment(
                amount=created_booking.total_amount
            )
            if not success:
                self._booking_service.cancel_booking(created_booking.booking_id)
                raise ValueError("Payment not successful")

            self._booking_service.confirm_booking(created_booking.booking_id)
            ticket = self._ticket_generation_service.generate_ticket(
                booking=created_booking
            )
            self._ticket_generation_service.print_ticket(ticket_id=ticket.ticket_id)
            return ticket

        except ValueError as e:

            print(f"Booking failed: {e}")

    def cancel_booking(self, booking_id):
        self._booking_service.cancel_booking(booking_id=booking_id)
