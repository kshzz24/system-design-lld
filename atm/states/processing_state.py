from __future__ import annotations
from typing import TYPE_CHECKING

from states.atm_state import ATMState
from models.card import Card
from constants.transaction import OperationType

if TYPE_CHECKING:
    from atm import ATMSystem


class ProcessingState(ATMState):

    def insert_card(self, atm: ATMSystem, card: Card) -> None:
        print("Card already inserted")

    def enter_pin(self, atm: ATMSystem, pin: str) -> None:
        print("PIN already inserted")

    def select_operation(self, atm: ATMSystem, op: OperationType) -> None:
        from states.dispensing_state import DispensingState

        card = atm.session.card
        if op == OperationType.WITHDRAW:
            amount = atm.session.amount
            if amount is None:
                print("No amount specified")
                return
            # Check the machine can dispense BEFORE touching the account, so we
            # never debit money we can't physically hand out.
            if not atm.cash_dispense.has_sufficient_cash(int(amount)):
                print("ATM cannot dispense this amount")
                return
            success = atm.bank_service.withdraw(card, amount)
            if success:
                dispensing = DispensingState()
                atm.set_state(dispensing)
                dispensing.dispense(atm)
            else:
                print("Withdrawal failed: insufficient funds")
        elif op == OperationType.DEPOSIT:
            amount = atm.session.amount
            atm.bank_service.deposit(card, amount)
        elif op == OperationType.CHECK_BALANCE:
            balance = atm.bank_service.get_balance(card)
            print(f"Balance: {balance}")
        else:
            print("Please select Valid Operation")

    def cancel(self, atm: ATMSystem) -> None:
        from states.idle_state import IdleState

        print("Cancelling, ejecting card")
        atm.session.end_session()
        atm.set_state(IdleState())
