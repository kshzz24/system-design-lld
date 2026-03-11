from states.game_state import GameState


class DrawState(GameState):
      def handle_move(self, game, player, row, col):
        print("Game is already over. It's a draw!")