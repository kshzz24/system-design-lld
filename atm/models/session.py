from models.card import Card
from datetime import datetime
from models.transaction import Transaction



class Session:
    session_id: str
    card: Card
    start_time: datetime
    end_time: datetime | None
    is_authenticated: bool
    transactions: list[Transaction]
    amount: float | None

    def __init__(self, session_id:str, card: Card):
        self.session_id = session_id
        self.card = card
        self.start_time = datetime.now()
        self.end_time = None
        self.is_authenticated = False
        self.transactions = []
        self.amount = None
    
    def add_transaction(self, transaction:Transaction)->None:
        self.transactions.append(transaction)

    def end_session(self)->None:
        self.is_authenticated = False
        self.end_time = datetime.now()
    
    def is_active(self)->bool:
        return self.is_authenticated

