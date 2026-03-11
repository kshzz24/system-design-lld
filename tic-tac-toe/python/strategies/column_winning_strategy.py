
from strategies.winning_strategy import WinningStrategy

class ColumnWinningStrategy(WinningStrategy):
      
      def check_winner(self,board, row, col, symbol)->bool:
           size = len(board[0])
           for i in range (size):
               if board[i][col].symbol != symbol:  
                    return False
           return True



