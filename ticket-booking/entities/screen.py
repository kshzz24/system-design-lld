from enums.enums import ScreenType
from dataclasses import dataclass

@dataclass
class Screen:
    screen_id:str
    name:str
    screen_type:ScreenType