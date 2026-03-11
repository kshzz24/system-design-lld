
from strategies.winning_strategy import WinningStrategy

class RowWinningStrategy(WinningStrategy):
      
      def check_winner(self,board, row, col, symbol)->bool:
           size = len(board[0])
           for j in range (size):
               if board[row][j].symbol != symbol:  
                    return False
           return True



