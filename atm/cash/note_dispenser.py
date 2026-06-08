from __future__ import annotations
from abc import ABC, abstractmethod


class NoteDispenser(ABC):

    num_notes: int
    next_handler: NoteDispenser | None

    def __init__(self, num_notes: int) -> None:
        self.num_notes = num_notes
        self.next_handler = None

    @property
    @abstractmethod
    def note_value(self) -> int:
        """The denomination this handler dispenses (e.g. 500)."""
        ...

    def set_next(self, handler: NoteDispenser) -> None:
        self.next_handler = handler

    def can_handle(self, amount: int) -> bool:
      
        return amount >= self.note_value and self.num_notes > 0

    def dispense(self, amount: int) -> int:
        """Dispense from this denomination, forward the remainder down the chain.

        Returns the amount that could NOT be dispensed (0 means fully served).
        """
        remaining = amount
        if self.can_handle(remaining):
            notes_to_give = min(remaining // self.note_value, self.num_notes)
            self.num_notes -= notes_to_give
            remaining -= notes_to_give * self.note_value
            print(f"  Dispensed {notes_to_give} x {self.note_value}")
        if remaining > 0 and self.next_handler is not None:
            return self.next_handler.dispense(remaining)
        return remaining
