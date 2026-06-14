from repositories.show_repository import ShowRepository
import threading
from enums.enums import SeatStatus
from datetime import datetime
from entities.seat import Seat


class SeatService:

    def __init__(self, show_repo: ShowRepository):
        self._show_repo = show_repo
        self._lock = threading.Lock()

    def lock_seat(self, show_id: str, seat_id: str, user_id: str) -> bool:
        show = self._show_repo.find_by_id(show_id=show_id)
        if not show:
            raise ValueError(f"Show with {show_id} ID not found")

        current_seat = None
        for seat in show.seats:
            if seat.seat_id == seat_id:
                current_seat = seat

        if not current_seat:
            raise ValueError(f"Seat with {seat_id} ID not found")

        with self._lock:
            if current_seat.status == SeatStatus.AVAILABLE:
                current_seat.status = SeatStatus.LOCKED
                current_seat.locked_by = user_id
                current_seat.locked_at = datetime.now()
                return True
            return False

    def release_seat(self, show_id: str, seat_id: str) -> None:
        show = self._show_repo.find_by_id(show_id=show_id)
        if not show:
            raise ValueError(f"Show with {show_id} ID not found")

        current_seat = None
        for seat in show.seats:
            if seat.seat_id == seat_id:
                current_seat = seat
        if not current_seat:
            raise ValueError(f"Seat with {seat_id} ID not found")

        with self._lock:
            if current_seat.status in (SeatStatus.LOCKED, SeatStatus.BOOKED):
                current_seat.status = SeatStatus.AVAILABLE
                current_seat.locked_by = None
                current_seat.locked_at = None

    def check_availability(self, show_id: str) -> list[Seat]:
        show = self._show_repo.find_by_id(show_id=show_id)
        if not show:
            raise ValueError(f"Show with {show_id} ID not found")

        return [s for s in show.seats if s.status == SeatStatus.AVAILABLE]
