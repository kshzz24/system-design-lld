from datetime import datetime
from entities.movie import Movie
from entities.screen import Screen
from entities.seat import Seat
from dataclasses import dataclass,field


@dataclass
class Show:
    show_id: str
    movie: Movie
    screen: Screen
    theatre_id:str
    start_time: datetime
    seats: list[Seat] = field(default_factory=list)
