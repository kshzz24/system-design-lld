from repositories.theatre_repository import TheatreRepository
from repositories.show_repository import ShowRepository
from repositories.movie_repository import MovieRepository
from entities.theatre import Theatre
from entities.show import Show
from entities.screen import Screen
from entities.movie import Movie


class AdminService:
    def __init__(
        self,
        theatre_repo: TheatreRepository,
        show_repo: ShowRepository,
        movie_repo: MovieRepository,
    ) -> None:
        self._theatre_repo = theatre_repo
        self._show_repo = show_repo
        self._movie_repo = movie_repo

    def add_movie(self, movie: Movie) -> None:
        self._movie_repo.save(movie=movie)

    def add_theatre(self, theatre: Theatre) -> None:
        self._theatre_repo.save(theatre=theatre)

    def add_screen(self, theatre_id: str, screen: Screen) -> None:
        theatre = self._theatre_repo.find_by_id(theatre_id=theatre_id)
        if not theatre:
            raise ValueError(f"No theatre with id {theatre_id}")
        theatre.screens.append(screen)
        self._theatre_repo.save(theatre=theatre)

    def add_show(self, show: Show) -> None:
        self._show_repo.save(show=show)
