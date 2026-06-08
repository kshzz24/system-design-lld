from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from models.card import Card
from constants.transaction import OperationType

if TYPE_CHECKING:
    from atm import ATMSystem


class ATMState(ABC):
    @abstractmethod
    def insert_card(self, atm: ATMSystem, card: Card) -> None:
        pass

    @abstractmethod
    def enter_pin(self, atm: ATMSystem, pin: str) -> None:
        pass

    @abstractmethod
    def select_operation(self, atm: ATMSystem, op: OperationType) -> None:
        pass

    @abstractmethod
    def cancel(self, atm: ATMSystem) -> None:
        pass
