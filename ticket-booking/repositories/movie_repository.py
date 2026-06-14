from abc import ABC, abstractmethod
from entities.movie import Movie
from typing import Optional


class MovieRepository(ABC):

    @abstractmethod
    def save(self, movie: Movie) -> None:
        pass

    @abstractmethod
    def find_by_id(self, movie_id: str) -> Optional[Movie]:
        pass


class InMemoryMovieRepository(MovieRepository):

    def __init__(self) -> None:
        self._store: dict[str, Movie] = {}

    def save(self, movie: Movie) -> None:
        self._store[movie.movie_id] = movie

    def find_by_id(self, movie_id: str) -> Optional[Movie]:
        return self._store.get(movie_id)
