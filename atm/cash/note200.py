from __future__ import annotations
from cash.note_dispenser import NoteDispenser


class Note200(NoteDispenser):
    """Handler for 200 notes."""

    @property
    def note_value(self) -> int:
        return 200
