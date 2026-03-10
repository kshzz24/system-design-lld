
from symbol import Symbol
class Cell:

    def __init__(self):
       self._symbol = Symbol.EMPTY

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: Symbol):
        self._symbol = symbol