import datetime

class Card:
    card_number:str
    pin_hash:str
    is_blocked:bool
    pin_attempt_count:int
    expiry_date: datetime.date
 

    def __init__(self, card_number:str, pin_hash:str, expiry_date:datetime.date)->None:
        self.card_number = card_number
        self.pin_hash = pin_hash
        self.expiry_date = expiry_date
        self.is_blocked  = False
        self.pin_attempt_count = 0

