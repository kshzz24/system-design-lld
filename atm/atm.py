from __future__ import annotations

from states.atm_state import ATMState
from states.idle_state import IdleState
from services.bank_service import BankService
from cash.cash_dispense import CashDispense
from models.session import Session
from models.card import Card
from constants.transaction import OperationType


class ATMSystem:
    """The ATM controller (Context of the State pattern).

    Holds its collaborators (bank facade + cash dispenser), the current
    session, and the current state. Every public action simply forwards to
    the current state, which decides what to do and which state comes next.
    """

    current_state: ATMState
    bank_service: BankService
    cash_dispense: CashDispense
    session: Session | None

    def __init__(self, bank_service: BankService, cash_dispense: CashDispense) -> None:
        self.bank_service = bank_service
        self.cash_dispense = cash_dispense
        self.session = None
        self.current_state = IdleState()

    def set_state(self, state: ATMState) -> None:
        print(f"[STATE] {type(self.current_state).__name__} -> {type(state).__name__}")
        self.current_state = state

    # --- forwarding API: delegate every action to the current state ---

    def insert_card(self, card: Card) -> None:
        self.current_state.insert_card(self, card)

    def enter_pin(self, pin: str) -> None:
        self.current_state.enter_pin(self, pin)

    def select_operation(self, op: OperationType) -> None:
        self.current_state.select_operation(self, op)

    def cancel(self) -> None:
        self.current_state.cancel(self)
