from __future__ import annotations
from typing import TYPE_CHECKING

from states.atm_state import ATMState
from models.card import Card
from constants.transaction import OperationType

if TYPE_CHECKING:
    from atm import ATMSystem


class CardInsertedState(ATMState):

    def insert_card(self, atm: ATMSystem, card: Card) -> None:
        print("Card already inserted")

    def enter_pin(self, atm: ATMSystem, pin: str) -> None:
        from states.idle_state import IdleState
        from states.processing_state import ProcessingState

        card = atm.session.card
        success = atm.bank_service.authenticate(card, pin)
        if success:
            atm.session.is_authenticated = True
            print("PIN verified")
            atm.set_state(ProcessingState())
        else:
            if card.is_blocked:
                print("Card blocked after too many attempts")
                atm.set_state(IdleState())
            else:
                print(f"Wrong PIN. Attempts: {card.pin_attempt_count}")

    def select_operation(self, atm: ATMSystem, op: OperationType) -> None:
        print("Please enter PIN first")

    def cancel(self, atm: ATMSystem) -> None:
        from states.idle_state import IdleState

        print("Cancelling, ejecting card")
        atm.session.end_session()
        atm.set_state(IdleState())
