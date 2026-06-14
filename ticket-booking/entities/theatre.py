from entities.screen import Screen
from entities.city import City
from dataclasses import dataclass, field


@dataclass
class Theatre:
    theatre_id: str
    theatre_name: str
    address: str
    city: City
    screens: list[Screen] = field(default_factory=list)
