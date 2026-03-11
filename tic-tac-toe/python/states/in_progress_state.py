from states.game_state import GameState
from states.winner_state import WinnerState
from states.draw_state import DrawState
from models.game_status import GameStatus
from models.symbol import Symbol


class InProgressState(GameState):
      def handle_move(self, game, player, row, col):
          if not game.board.place_symbol(row, col, player.symbol):
                return False
          
          is_player_won = game.check_winner(player, row, col, player.symbol)
          is_board_full = game.board.is_full()

          if is_player_won:
               game.state = WinnerState()
               game.winner = player
               if player.symbol == Symbol.X:
                   game.status = GameStatus.WINNER_X
               else:
                   game.status = GameStatus.WINNER_O
               game.notify_observers()  
          elif is_board_full:
               game.state = DrawState()
               game.status = GameStatus.DRAW
               game.notify_observers()  
          else:
               game.switch_player()
