from vending_state import VendingMachineState


from inventory.item import Item


class DispenseState(VendingMachineState):
     
     def __init__(self, machine):
          super().__init__()
          from vending_machine import VendingMachine
          self._vending_machine:VendingMachine = machine

     def select_item(self, item):
           print("Machine busy, please wait")
     
     def insert_coin(self, coin):      
           print("Machine busy, please wait")

     def insert_note(self, note):      
           print("Machine busy, please wait")
     
     def dispense(self):
      
         vending_machine = self._vending_machine
         item:Item  = vending_machine.get_selected_item()
         print(f"Dispensing {item.name}...")
         change_amt = vending_machine.balance
         if change_amt > 0:
              change = vending_machine.calculate_change(change_amt)
              print(change)
         vending_machine.reset()  
       
     
     def refund(self):
         print("Item already dispensed, cannot refund")
