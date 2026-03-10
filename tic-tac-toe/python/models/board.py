from models.cell import Cell
from models.symbol import Symbol
class Board:


    def __init__(self, size):
        self.size = size
        self._moves_count  = 0 
        self.initialize_board()
        
    def initialize_board(self):
        self.board = [[Cell() for _ in range(self.size)] for _ in range(self.size)]
    
    def is_full(self)->bool:
         _size = self.size
         return self._moves_count == _size*_size
    def get_cell(self, row, col):
        return self.board[row][col]
    
    def place_symbol(self, row, col, symbol)->bool:
        if row < 0 or row >= self.size or col < 0 or col>= self.size:
             return False
        
        if self.board[row][col].symbol == Symbol.EMPTY:
            self.board[row][col].symbol = symbol
            self._moves_count += 1
            return True
        
        return False
    
    def print_board(self):
      for i in range(self.size):
          row = " | ".join(self.board[i][j].symbol.get_char() 
          for j  in range(self.size))
          print(row)
          if i < self.size - 1:
              print("-" * (self.size * 4 - 3))

            


