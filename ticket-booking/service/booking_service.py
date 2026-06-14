from repositories.booking_repository import BookingRepository

from service.seat_service import SeatService
from service.payment_service import PaymentService
from entities.seat import Seat
from entities.show import Show
from entities.user import User
from entities.booking import Booking
from enums.enums import BookingStatus
from datetime import datetime, timedelta
import uuid
from enums.enums import SeatStatus


class BookingService:

    def __init__(
        self,
        booking_repo: BookingRepository,
        seat_service: SeatService,
        payment_service: PaymentService,
    ):
        self._booking_repo = booking_repo
        self._seat_service = seat_service
        self._payment_service = payment_service

    def create_booking(self, user: User, show: Show, seats: list[Seat]) -> Booking:

        user_id = user.user_id
        show_id = show.show_id

        locked: list[Seat] = []
        for seat in seats:
            if not self._seat_service.lock_seat(
                show_id=show_id, seat_id=seat.seat_id, user_id=user_id
            ):
                for s in locked:
                    self._seat_service.release_seat(show_id=show_id, seat_id=s.seat_id)
                raise ValueError("Some seats are unavailable")
            locked.append(seat)

        total_amount = self._payment_service.calculate_total(seats=seats)

        booking: Booking = Booking(
            booking_id=str(uuid.uuid4()),
            user=user,
            show=show,
            status=BookingStatus.PENDING,
            total_amount=total_amount,
            created_at=datetime.now(),
            seats=locked,
            expires_at=datetime.now() + timedelta(minutes=10),
        )

        self._booking_repo.save(booking=booking)
        return booking

    def confirm_booking(self, booking_id: str) -> bool:
        booking_details = self._booking_repo.find_by_id(booking_id=booking_id)

        if not booking_details:
            raise ValueError("Current Booking is not present")

        booking_status = booking_details.status

        if booking_status != BookingStatus.PENDING:
            return False

        for seat in booking_details.seats:
            seat.status = SeatStatus.BOOKED

        booking_details.status = BookingStatus.CONFIRMED

        return True

    def cancel_booking(self, booking_id: str) -> bool:
        booking_details = self._booking_repo.find_by_id(booking_id=booking_id)
        if not booking_details:
            raise ValueError("Current Booking is not present")
        booking_status = booking_details.status
        show = booking_details.show

        if (
            booking_status != BookingStatus.CONFIRMED
            and booking_status != BookingStatus.PENDING
        ):
            return False

        if booking_status == BookingStatus.CONFIRMED:
            amount_to_refund = booking_details.total_amount
            self._payment_service.initiate_refund(amount=amount_to_refund)

        for seat in booking_details.seats:
            self._seat_service.release_seat(show_id=show.show_id, seat_id=seat.seat_id)

        booking_details.status = BookingStatus.CANCELLED

        return True

    def get_booking(self, booking_id: str) -> Booking:
        booking_details = self._booking_repo.find_by_id(booking_id=booking_id)
        if not booking_details:
            raise ValueError("Current Booking is not Available")

        return booking_details

    def expire_booking(self, booking_id: str) -> None:
        booking_details = self._booking_repo.find_by_id(booking_id=booking_id)
        if not booking_details:
            raise ValueError("Current Booking is not Available")
        show = booking_details.show

        if booking_details.status == BookingStatus.PENDING and (
            datetime.now() > booking_details.expires_at
        ):
            seats_locked = booking_details.seats
            for seat in seats_locked:
                self._seat_service.release_seat(
                    show_id=show.show_id, seat_id=seat.seat_id
                )

            booking_details.status = BookingStatus.FAILED
