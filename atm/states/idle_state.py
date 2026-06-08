from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atm import ATMSystem

from states.atm_state import ATMState
from states.card_inserted import CardInsertedState
from models.card import Card
from models.session import Session
import uuid
from constants.transaction import OperationType


class IdleState(ATMState):

    def __init__(self) -> None:
        pass

    def insert_card(self, atm: ATMSystem, card: Card) -> None:

        session = Session(session_id=str(uuid.uuid4()), card=card)
        atm.session = session
        print("Card Inserted Successfully")
        atm.set_state(CardInsertedState())

    def enter_pin(self, atm: ATMSystem, pin: str) -> None:
        print("Please Enter the card!")

    def select_operation(self, atm: ATMSystem, op: OperationType) -> None:
        print("Please Enter the card!")

    def cancel(self, atm: ATMSystem) -> None:
        print("Please Enter the card")
