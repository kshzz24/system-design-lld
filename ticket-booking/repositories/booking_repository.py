from abc import ABC, abstractmethod
from entities.booking import Booking
from typing import Optional


class BookingRepository(ABC):

    @abstractmethod
    def save(self, booking: Booking) -> None:
        pass

    @abstractmethod
    def find_by_id(self, booking_id: str) -> Optional[Booking]:
        pass


class InMemoryBookingRepository(BookingRepository):

    def __init__(self) -> None:
        self._store: dict[str, Booking] = {}

    def save(self, booking: Booking) -> None:
        self._store[booking.booking_id] = booking

    def find_by_id(self, booking_id: str) -> Optional[Booking]:
        return self._store.get(booking_id)
