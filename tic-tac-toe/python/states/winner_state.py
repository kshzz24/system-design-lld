from states.game_state import GameState


class WinnerState(GameState):
      def handle_move(self, game, player, row, col):
        print("Game is already over. We have a winner!")