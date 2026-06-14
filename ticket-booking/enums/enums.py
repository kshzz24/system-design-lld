from enum import Enum


class BookingStatus(Enum):

    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


class SeatType(Enum):
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"


class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    LOCKED = "LOCKED"
    BOOKED = "BOOKED"


class ScreenType(Enum):

    STANDARD = "STANDARD"
    IMAX = "IMAX"
    DOLBY = "DOLBY"


class PaymentType(Enum):

    UPI = "UPI"
    DEBIT = "DEBIT"
    CREDIT = "CREDIT"
