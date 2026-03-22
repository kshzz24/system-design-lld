
import threading
from states.idle_state import IdleState
from money import Coin, Note
from inventory.inventory import Inventory
from inventory.item import Item


class VendingMachine:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.state = IdleState(self)
        self.inventory = Inventory()
        self.balance = 0
        self.selected_item_code = ""
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                     cls._instance = VendingMachine() 

        return cls._instance
    
    #money
    def insert_coin(self, coin:Coin):
        return self.state.insert_coin(coin)
    
    def insert_note(self, note:Note):
        return self.state.insert_note(note)
    
    def add_balance(self, amt: int):
         self.balance += amt
    
    def refund_balance(self):
        self.state.refund()

    def select_item(self, item_code:str):
         self.state.select_item(item_code)
         
    
    def dispense(self):
         self.state.dispense()
    
    def add_item(self, code, name, price, quantity):
        item = Item(price, code, name)
        self.inventory.add_item(code, item, quantity)

    def set_selected_item_code(self,code):
        self.selected_item_code = code

    def get_selected_item(self):
         return self.inventory.get_item(self.selected_item_code)

    def calculate_change(self, amt):
        change = []

        # Notes (in descending order)
        notes_values = [2000, 1000, 500, 100]  # TWENTY, TEN, FIVE, ONE
        notes_enum = {2000: Note.TWENTY, 1000: Note.TEN, 500: Note.FIVE, 100: Note.ONE}

        # Coins (in descending order)
        coins_values = [25, 10, 5, 1]  # QUARTER, DIME, NICKEL, PENNY
        coins_enum = {25: Coin.QUARTER, 10: Coin.DIME, 5: Coin.NICKEL, 1: Coin.PENNY}

        # Process notes first (greedy algorithm)
        for note_val in notes_values:
            while amt >= note_val:
                change.append(notes_enum[note_val])
                amt -= note_val

        # Process coins
        for coin_val in coins_values:
            while amt >= coin_val:
                change.append(coins_enum[coin_val])
                amt -= coin_val

        return change

    def reset(self):
        self.balance = 0
        self.selected_item_code = ""
        self.state = IdleState(self)


