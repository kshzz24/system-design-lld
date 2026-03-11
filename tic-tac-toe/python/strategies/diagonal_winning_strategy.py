
from strategies.winning_strategy import WinningStrategy

class DiagonalWinningStrategy(WinningStrategy):
      
    def check_winner(self, board, row, col, symbol) -> bool:        
        size = len(board[0])

        # Check main diagonal (\)
        if row == col:
            if all(board[i][i].symbol == symbol for i in
    range(size)):
                return True

        # Check anti-diagonal (/)
        if row + col == size - 1:
            if all(board[i][size - i - 1].symbol == symbol for i in 
    range(size)):
                return True

        return False

