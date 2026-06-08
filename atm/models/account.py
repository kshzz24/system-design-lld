
# from enum import Enum
from constants.account_type import AccountType

class Account:
    account_id: str
    account_type: AccountType
    linked_cards: list[str]
    balance:float

    def __init__ (self, account_id:str, account_type:AccountType, linked_card:str, balance:float):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance
        self.linked_cards = []
        self.linked_cards.append(linked_card)

    
    def debit(self, amount:float)->bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False
    
    def credit(self, amount:float)->None:
        self.balance += amount
    
    def get_balance(self)->float:
        return self.balance

