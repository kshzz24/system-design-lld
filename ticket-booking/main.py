"""
Movie Ticket Booking System — Integration / Composition Root.

This file is the COMPOSITION ROOT: the one place where concrete objects are
created and dependencies are wired together (repos -> services -> facade).
Everything below the facade depends only on abstractions; here we pick the
concrete InMemory implementations and inject them.

Run: python main.py
"""

from datetime import datetime, timedelta

# Repositories (concrete in-memory implementations)
from repositories.theatre_repository import InMemoryTheatreRepository
from repositories.show_repository import InMemoryShowRepository
from repositories.movie_repository import InMemoryMovieRepository
from repositories.booking_repository import InMemoryBookingRepository

# Services
from service.admin_service import AdminService
from service.search_service import SearchService
from service.seat_service import SeatService
from service.payment_service import PaymentService
from service.booking_service import BookingService
from service.ticket_generation_service import TicketGenerationService
from service.ticket_booking_service import TicketBookingSystem

# Payment strategies
from payment.upi_payment import UPIPayment
from payment.credit_payment import CreditPayment

# Entities & enums
from entities.city import City
from entities.theatre import Theatre
from entities.screen import Screen
from entities.movie import Movie
from entities.show import Show
from entities.seat import Seat
from entities.user import User
from enums.enums import SeatType, ScreenType, SeatStatus


def make_seats() -> list[Seat]:
    """Build a small block of seats for a screen/show."""
    return [
        Seat("st1", SeatType.SILVER, "A1", 150.0),
        Seat("st2", SeatType.SILVER, "A2", 150.0),
        Seat("st3", SeatType.GOLD, "B1", 250.0),
        Seat("st4", SeatType.GOLD, "B2", 250.0),
        Seat("st5", SeatType.PLATINUM, "C1", 400.0),
    ]


def seat_states(seats: list[Seat]) -> list[str]:
    return [f"{s.seat_number}:{s.status.name}" for s in seats]


def main() -> None:
    # ---------------------------------------------------------------
    # COMPOSITION ROOT — wire repos -> services -> facade
    # ---------------------------------------------------------------
    theatre_repo = InMemoryTheatreRepository()
    show_repo = InMemoryShowRepository()
    movie_repo = InMemoryMovieRepository()
    booking_repo = InMemoryBookingRepository()

    admin_service = AdminService(theatre_repo, show_repo, movie_repo)
    search_service = SearchService(theatre_repo, show_repo, movie_repo)
    seat_service = SeatService(show_repo)
    # PaymentService here is only used by BookingService for calculate_total
    # (strategy is irrelevant for totals); per-transaction strategy is chosen
    # at book time inside the facade.
    payment_service = PaymentService(UPIPayment("system@upi", "0000"))
    booking_service = BookingService(booking_repo, seat_service, payment_service)
    ticket_service = TicketGenerationService()

    system = TicketBookingSystem(search_service, booking_service, ticket_service)

    # ---------------------------------------------------------------
    # STEP 1 — Admin sets up the catalog
    # ---------------------------------------------------------------
    print("\n=== STEP 1: Admin adds movie, theatre, screen, show ===")
    city = City("c1", "Mumbai", "MH")
    movie = Movie("Inception", "m1", "Christopher Nolan", 148)
    theatre = Theatre("t1", "PVR Phoenix", "Lower Parel", city)
    screen = Screen("scr1", "Audi 1", ScreenType.IMAX)
    seats = make_seats()
    show = Show("show1", movie, screen, "t1", datetime.now() + timedelta(hours=2), seats)

    admin_service.add_movie(movie)
    admin_service.add_theatre(theatre)
    admin_service.add_screen("t1", screen)
    admin_service.add_show(show)
    print(f"Added movie='{movie.movie_name}', theatre='{theatre.theatre_name}', "
          f"screen='{screen.name}', show='{show.show_id}' with {len(seats)} seats")

    # ---------------------------------------------------------------
    # STEP 2 — User searches movies in a city
    # ---------------------------------------------------------------
    print("\n=== STEP 2: User searches in city 'c1' ===")
    theatres = system.search_movies("c1")
    print("Theatres in Mumbai:", [t.theatre_name for t in theatres])
    shows = system.get_shows_for_theatre("t1")
    print("Shows at PVR Phoenix:", [s.show_id for s in shows])

    # ---------------------------------------------------------------
    # STEP 3 — User 1 selects show, locks 2 seats, pays -> booked
    # ---------------------------------------------------------------
    print("\n=== STEP 3: User 1 books seats B1, B2 (pays with UPI) ===")
    user1 = User("Kashish", "u1", "kashish@mail.com", "9999999999")
    chosen = [seats[2], seats[3]]  # B1, B2
    ticket1 = system.book_tickets(user1, show, chosen, UPIPayment("kashish@oksbi", "1234"))
    print("Ticket issued:", ticket1.ticket_id[:8] if ticket1 else None)

    # ---------------------------------------------------------------
    # STEP 4 — Verify seat status changed to BOOKED
    # ---------------------------------------------------------------
    print("\n=== STEP 4: Verify seats are BOOKED ===")
    print("Seat states:", seat_states(seats))
    print("Available seats now:", [s.seat_number for s in seat_service.check_availability("show1")])

    # ---------------------------------------------------------------
    # STEP 5 — User 2 tries the SAME seats -> unavailable
    # ---------------------------------------------------------------
    print("\n=== STEP 5: User 2 tries the same seats B1, B2 ===")
    user2 = User("Rahul", "u2", "rahul@mail.com", "8888888888")
    ticket2 = system.book_tickets(user2, show, chosen, CreditPayment("4111111111111111", "123"))
    print("User 2 ticket:", ticket2)  # expected None (booking failed)

    # ---------------------------------------------------------------
    # STEP 6 — User 1 cancels -> seats released -> User 2 books
    # ---------------------------------------------------------------
    print("\n=== STEP 6: User 1 cancels, then User 2 books the freed seats ===")
    system.cancel_booking(ticket1.booking.booking_id)
    print("After cancel, seat states:", seat_states(seats))
    ticket3 = system.book_tickets(user2, show, chosen, CreditPayment("4111111111111111", "123"))
    print("User 2 ticket now:", ticket3.ticket_id[:8] if ticket3 else None)
    print("Seat states:", seat_states(seats))

    # ---------------------------------------------------------------
    # STEP 7 — 10-minute timeout: lock seats, expire booking, verify released
    # ---------------------------------------------------------------
    print("\n=== STEP 7: Expiry — a PENDING booking past its window releases seats ===")
    platinum = [seats[4]]  # C1
    pending = booking_service.create_booking(user1, show, platinum)
    print("Created PENDING booking, seat states:", seat_states(platinum))
    # Simulate that 10 minutes have already passed:
    pending.expires_at = datetime.now() - timedelta(minutes=1)
    booking_service.expire_booking(pending.booking_id)
    print("After expire, seat states:", seat_states(platinum),
          "| booking status:", booking_service.get_booking(pending.booking_id).status.name)

    print("\n=== Simulation complete ===")


if __name__ == "__main__":
    main()
