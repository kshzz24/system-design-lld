
from vending_state import VendingMachineState
from money import Coin, Note
from states.idle_state import IdleState

class HasMoneyState(VendingMachineState):
    
    def __init__(self, machine):
        super().__init__()
        self._vending_machine = machine

    def select_item(self, item_code:str)->None:
        from states.item_selected import ItemSelectedState

        current_machine = self._vending_machine
        
        if item_code not in current_machine.inventory.item_map:
            print(f"Item {item_code} not available")
            return

        # Get the item
        item = current_machine.inventory.item_map[item_code]

        # Check if enough balance
        if current_machine.balance >= item.price:
            # Store the selected item code
            current_machine.selected_item_code = item_code
            # Transition to ItemSelectedState
            current_machine.state = ItemSelectedState(current_machine)
        else:
            print(f"Insufficient balance. Item costs {item.price}, you have {current_machine.balance}")

    def insert_coin(self, coin:Coin)->None:
        self._vending_machine.balance += coin.value
       
    
    def insert_note(self, note:Note):
        self._vending_machine.balance += note.value
    
    def dispense(self):
        pass
    
    def refund(self):
        vending_machine = self._vending_machine
        balance = vending_machine.balance
        change = vending_machine.calculate_change(balance)
        print(f"Refunding: {change}")
        vending_machine.balance = 0
        vending_machine.state = IdleState(vending_machine)
         