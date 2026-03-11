from abc import ABC,abstractmethod


class GameState(ABC):
    @abstractmethod
    def handle_move(self, game, player, row, col):
          pass