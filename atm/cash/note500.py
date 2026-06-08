from __future__ import annotations
from cash.note_dispenser import NoteDispenser


class Note500(NoteDispenser):

    @property
    def note_value(self) -> int:
        return 500
