from abc import ABC, abstractmethod
from entities.theatre import Theatre
from typing import Optional


class TheatreRepository(ABC):

    @abstractmethod
    def save(self, theatre: Theatre) -> None:
        pass

    @abstractmethod
    def find_by_id(self, theatre_id: str) -> Optional[Theatre]:
        pass

    @abstractmethod
    def find_by_city(self, city_id: str) -> list[Theatre]:
        pass


class InMemoryTheatreRepository(TheatreRepository):

    def __init__(self) -> None:
        self._store: dict[str, Theatre] = {}

    def save(self, theatre: Theatre) -> None:
        self._store[theatre.theatre_id] = theatre

    def find_by_id(self, theatre_id: str) -> Optional[Theatre]:
        return self._store.get(theatre_id)

    def find_by_city(self, city_id: str) -> list[Theatre]:
     
        return [
            theatre
            for theatre in self._store.values()
            if theatre.city.city_id == city_id
        ]
