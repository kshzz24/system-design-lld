from models.board import Board
from models.player import Player
from models.game_status import GameStatus
from models.symbol import Symbol
from strategies.winning_strategy import WinningStrategy
from strategies.column_winning_strategy import ColumnWinningStrategy
from strategies.row_winning_strategy import RowWinningStrategy
from strategies.diagonal_winning_strategy import DiagonalWinningStrategy

class Game:
    board:Board
    player1: Player
    player2:Player
    current_player:Player
    winner:Player
    status: GameStatus
    winning_strategies:list[WinningStrategy]

    def __init__(self, player1, player2, board_size):
        self.board = Board(board_size)
        self.player1 = player1
        self.player2 = player2
        self.current_player = player1
        self.status = GameStatus.IN_PROGRESS
        self.winning_strategies = [
            ColumnWinningStrategy(), 
            RowWinningStrategy(), 
            DiagonalWinningStrategy()]

   
    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1    

    def check_winner(self, player:Player, row:int, col:int, symbol:Symbol):
         
        strategies = self.winning_strategies
      
        for strategy in strategies:
            if strategy.check_winner(self.board.board, row, col,symbol):
                return True 
        return False    
        

    def make_move(self, row, col):
        if not self.board.place_symbol(row, col, self.current_player.symbol):
            return False

        current_player_won = self.check_winner(self.current_player, row, col, self.current_player.symbol)

        if current_player_won:
            self.winner = self.current_player
            if self.current_player.symbol == Symbol.X:
                self.status = GameStatus.WINNER_X
            else:
                self.status = GameStatus.WINNER_O
        elif self.board.is_full():
            self.status = GameStatus.DRAW
        else:
            self.switch_player()


        


