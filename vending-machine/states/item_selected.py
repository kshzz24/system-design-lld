from vending_state import VendingMachineState




class ItemSelectedState(VendingMachineState):
    def __init__(self, machine):
        super().__init__()
        from vending_machine import VendingMachine
        self._vending_machine:VendingMachine = machine
    
    def select_item(self, item_code):
        vending_machine = self._vending_machine
        vending_machine.set_selected_item_code(item_code)
    
    def insert_coin(self, coin):
        self._vending_machine.balance += coin.value
    
    def insert_note(self, note):
        self._vending_machine.balance += note.value
    
    def dispense(self):
        from states.dispensing import DispenseState
        vending_machine = self._vending_machine
        current_balance = vending_machine.balance
        current_selected_item = vending_machine.inventory.get_item(vending_machine.selected_item_code)

        if current_balance >= current_selected_item.price:
             vending_machine.balance -= current_selected_item.price
             current_item_code = current_selected_item.code
             vending_machine.inventory.reduce_stock(current_item_code)
             vending_machine.state = DispenseState(vending_machine)
             vending_machine.state.dispense()
    
    def refund(self):
         from states.idle_state import IdleState
         vending_machine = self._vending_machine
         
         balance = vending_machine.balance 
         vending_machine.calculate_change(balance)
         vending_machine.balance = 0
         vending_machine.state = IdleState(vending_machine)








         