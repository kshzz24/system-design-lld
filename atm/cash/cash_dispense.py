from __future__ import annotations
from cash.note_dispenser import NoteDispenser
from cash.note500 import Note500
from cash.note200 import Note200
from cash.note100 import Note100


class CashDispense:
    """Builds and drives the 500 -> 200 -> 100 dispensing chain.

    This is the client of the Chain of Responsibility. It owns the handlers,
    wires them together, and exposes a simple API to the rest of the system
    (the ATM states call `has_sufficient_cash` / `dispense_cash`).
    """

    handler_chain: NoteDispenser

    def __init__(self, num_500: int, num_200: int, num_100: int) -> None:
        self._note500 = Note500(num_500)
        self._note200 = Note200(num_200)
        self._note100 = Note100(num_100)
        self.build_chain()

    def build_chain(self) -> None:
        self._note500.set_next(self._note200)
        self._note200.set_next(self._note100)
        self.handler_chain = self._note500

    def has_sufficient_cash(self, amount: int) -> bool:
        """Dry-run the greedy chain WITHOUT mutating stock.

        Walks the same greedy algorithm `dispense` uses, but only reads the
        note counts. If this returns True, a subsequent `dispense_cash` is
        guaranteed to fully serve the amount, so we never deduct notes on a
        request we can't actually complete.
        """
        remaining = amount
        handler: NoteDispenser | None = self.handler_chain
        while handler is not None and remaining > 0:
            notes = min(remaining // handler.note_value, handler.num_notes)
            remaining -= notes * handler.note_value
            handler = handler.next_handler
        return remaining == 0

    def dispense_cash(self, amount: int) -> bool:
        """Validate, then dispense `amount`. Returns True on success."""
        if amount <= 0:
            print("Amount must be positive")
            return False
        if amount % 100 != 0:
            print("Amount must be in multiples of 100")
            return False
        if not self.has_sufficient_cash(amount):
            print("ATM cannot dispense this amount (insufficient notes)")
            return False
        remainder = self.handler_chain.dispense(amount)
        # Guaranteed 0 because has_sufficient_cash passed, but assert intent.
        return remainder == 0
