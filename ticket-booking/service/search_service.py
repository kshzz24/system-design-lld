from repositories.theatre_repository import TheatreRepository
from repositories.show_repository import ShowRepository
from repositories.movie_repository import MovieRepository
from entities.theatre import Theatre
from entities.show import Show
from typing import Optional


class SearchService:
    def __init__(
        self,
        theatre_repo: TheatreRepository,
        show_repo: ShowRepository,
        movie_repo: MovieRepository,
    ) -> None:
        self._theatre_repo = theatre_repo
        self._show_repo = show_repo
        self._movie_repo = movie_repo

    def select_city(self, city_id: str) -> list[Theatre]:
        return self._theatre_repo.find_by_city(city_id=city_id)

    def select_theatre(self, theatre_id: str) -> list[Show]:
        return self._show_repo.find_by_theatre(theatre_id=theatre_id)

    def select_movie(self, movie_id: str) -> list[Show]:
        return self._show_repo.find_by_movie(movie_id=movie_id)

    def select_show(self, show_id: str) -> Optional[Show]:
        return self._show_repo.find_by_id(show_id=show_id)
