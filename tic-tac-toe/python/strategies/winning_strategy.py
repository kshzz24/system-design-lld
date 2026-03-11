from abc import ABC, abstractmethod
from models.symbol import Symbol
from models.cell import Cell

class WinningStrategy(ABC):
      
      @abstractmethod
      def check_winner(self,board:list[list[Cell]], row:int, col:int, symbol:Symbol):
            pass