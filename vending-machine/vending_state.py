
from abc  import ABC, abstractmethod
from money import Coin, Note

class VendingMachineState(ABC):
          
     def __init__(self):
          pass

     @abstractmethod 
     def select_item(self, item:str)->None:
          pass
     @abstractmethod 
     def dispense(self)->None:
          pass
     @abstractmethod 
     def insert_coin(self, coin:Coin)->None:
          pass
     @abstractmethod 
     def insert_note(self, note:Note)->None:
          pass
     @abstractmethod 
     def refund(self)->None:
          pass