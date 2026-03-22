
from vending_state import VendingMachineState
from money import Coin, Note


class IdleState(VendingMachineState):

    def __init__(self, machine):
        super().__init__()
        self._vending_machine = machine

    def select_item(self, item:str)->None:
        print("Please Enter coin first")

    def insert_coin(self, coin:Coin)->None:
        from states.has_money import HasMoneyState
        current_machine = self._vending_machine
        current_machine.balance += coin.value
        current_machine.state = HasMoneyState(current_machine)

    def insert_note(self, note:Note):
        from states.has_money import HasMoneyState
        current_machine = self._vending_machine
        current_machine.balance += note.value
        current_machine.state = HasMoneyState(current_machine)
    
    def dispense(self):
        print("Invalid Operation")
    
    def refund(self):
        pass
         