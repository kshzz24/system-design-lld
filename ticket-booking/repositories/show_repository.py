from abc import ABC, abstractmethod
from entities.show import Show
from typing import Optional


class ShowRepository(ABC):

    @abstractmethod
    def save(self, show: Show) -> None:
        pass

    @abstractmethod
    def find_by_id(self, show_id: str) -> Optional[Show]:
        pass

    @abstractmethod
    def find_by_movie(self, movie_id: str) -> list[Show]:
        pass

    @abstractmethod
    def find_by_theatre(self, theatre_id: str) -> list[Show]:
        pass


class InMemoryShowRepository(ShowRepository):

    def __init__(self) -> None:
        self._store: dict[str, Show] = {}

    def save(self, show: Show) -> None:
        self._store[show.show_id] = show

    def find_by_id(self, show_id: str) -> Optional[Show]:
        return self._store.get(show_id)

    def find_by_movie(self, movie_id: str) -> list[Show]:
        return [s for s in self._store.values() if s.movie.movie_id == movie_id]

    def find_by_theatre(self, theatre_id: str) -> list[Show]:

        return [show for show in self._store.values() if show.theatre_id == theatre_id]
