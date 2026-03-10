from enum import Enum


class Symbol(Enum):
     X='X'
     O='O'
     EMPTY=' '
     def get_char(self) -> str:
         return self.value