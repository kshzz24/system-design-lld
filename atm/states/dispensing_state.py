from __future__ import annotations
from typing import TYPE_CHECKING
import uuid

from states.atm_state import ATMState
from models.card import Card
from models.transaction import Transaction
from constants.transaction import OperationType, TransactionStatus

if TYPE_CHECKING:
    from atm import ATMSystem


class DispensingState(ATMState):
    """The ATM is physically handing out cash.

    Cash availability has already been validated and the account already
    debited by ProcessingState, so `dispense` (the entry action of this state)
    only drives the Chain of Responsibility, records the transaction, prints a
    receipt, and ejects the card back to IdleState.

    While in this state the four interface actions are all rejected — the user
    cannot do anything until dispensing finishes.
    """

    def dispense(self, atm: ATMSystem) -> None:
        """Entry action: dispense notes, record the txn, eject."""
        from states.idle_state import IdleState

        amount = atm.session.amount
        print(f"Dispensing cash: {amount}")
        dispensed = atm.cash_dispense.dispense_cash(int(amount))

        txn = Transaction(
            transaction_id=str(uuid.uuid4()),
            operation_type=OperationType.WITHDRAW,
            amount=amount,
        )
        txn.status = (
            TransactionStatus.SUCCESS if dispensed else TransactionStatus.FAILED
        )
        atm.session.add_transaction(txn)
        print(txn.get_receipt())

        atm.session.amount = None
        print("Please collect your cash and card")
        atm.session.end_session()
        atm.set_state(IdleState())

    def insert_card(self, atm: ATMSystem, card: Card) -> None:
        print("Please wait, dispensing in progress")

    def enter_pin(self, atm: ATMSystem, pin: str) -> None:
        print("Please wait, dispensing in progress")

    def select_operation(self, atm: ATMSystem, op: OperationType) -> None:
        print("Please wait, dispensing in progress")

    def cancel(self, atm: ATMSystem) -> None:
        print("Cannot cancel, dispensing in progress")
