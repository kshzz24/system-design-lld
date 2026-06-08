from __future__ import annotations
from cash.note_dispenser import NoteDispenser


class Note100(NoteDispenser):
    """Handler for 100 notes — the tail of the chain."""

    @property
    def note_value(self) -> int:
        return 100
