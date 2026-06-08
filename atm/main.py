"""Entry point — wires the ATM together and runs the three demo scenarios.

This is a *scripted* simulation (no live input): main.py plays the role of the
user, so every action and amount is hardcoded to make the run repeatable and
the output verifiable.
"""

import datetime
import hashlib

from atm import ATMSystem
from services.bank_service import BankService
from cash.cash_dispense import CashDispense
from models.card import Card
from models.account import Account
from constants.account_type import AccountType
from constants.transaction import OperationType


def hash_pin(pin: str) -> str:
    """Hash a PIN the same way CardService.verify_pin does."""
    return hashlib.sha256(pin.encode()).hexdigest()


def banner(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    # --- Setup: build the ATM with 500x10, 200x10, 100x10 ---
    bank_service = BankService()
    cash_dispense = CashDispense(num_500=10, num_200=10, num_100=10)
    atm = ATMSystem(bank_service=bank_service, cash_dispense=cash_dispense)

    expiry = datetime.date(2030, 1, 1)

    # --- Scenario A: card that will be used to exhaust PIN attempts ---
    card_a = Card("CARD-A", hash_pin("1234"), expiry)
    account_a = Account("ACC-A", AccountType.SAVINGS, "CARD-A", 10000)
    bank_service.link_card(card_a, account_a)

    # --- Scenario B/C: a separate, fresh card ---
    card_b = Card("CARD-B", hash_pin("1234"), expiry)
    account_b = Account("ACC-B", AccountType.SAVINGS, "CARD-B", 10000)
    bank_service.link_card(card_b, account_b)

    # ============================================================
    banner("SCENARIO A: wrong PIN 3 times -> card blocked")
    # ============================================================
    atm.insert_card(card_a)
    for wrong_pin in ["0000", "1111", "2222"]:
        print(f"\n-> entering wrong PIN '{wrong_pin}'")
        atm.enter_pin(wrong_pin)
    print(f"\nCard A blocked? {card_a.is_blocked}")
    # A now-blocked card cannot authenticate even with the correct PIN:
    print("\n-> inserting blocked card and trying correct PIN '1234'")
    atm.insert_card(card_a)
    atm.enter_pin("1234")

    # ============================================================
    banner("SCENARIO B: successful withdrawal of 1300")
    # ============================================================
    atm.insert_card(card_b)
    atm.enter_pin("1234")
    print("\n-> user requests 1300")
    atm.session.amount = 1300
    atm.select_operation(OperationType.WITHDRAW)
    print(f"\nAccount B balance after withdrawal: {account_b.get_balance()}")

    # ============================================================
    banner("SCENARIO C: withdraw more than available -> graceful fail")
    # ============================================================
    atm.insert_card(card_b)
    atm.enter_pin("1234")
    print("\n-> user requests 50000 (exceeds funds/cash)")
    atm.session.amount = 50000
    atm.select_operation(OperationType.WITHDRAW)
    print(f"\nAccount B balance (unchanged): {account_b.get_balance()}")
    atm.cancel()


if __name__ == "__main__":
    main()


# ============================================================
# SAMPLE OUTPUT (python main.py)
# ============================================================
# ============================================================
# SCENARIO A: wrong PIN 3 times -> card blocked
# ============================================================
# Card Inserted Successfully
# [STATE] IdleState -> CardInsertedState
#
# -> entering wrong PIN '0000'
# Wrong PIN. Attempts: 1
#
# -> entering wrong PIN '1111'
# Wrong PIN. Attempts: 2
#
# -> entering wrong PIN '2222'
# Card blocked after too many attempts
# [STATE] CardInsertedState -> IdleState
#
# Card A blocked? True
#
# -> inserting blocked card and trying correct PIN '1234'
# Card Inserted Successfully
# [STATE] IdleState -> CardInsertedState
# Card blocked after too many attempts
# [STATE] CardInsertedState -> IdleState
#
# ============================================================
# SCENARIO B: successful withdrawal of 1300
# ============================================================
# Card Inserted Successfully
# [STATE] IdleState -> CardInsertedState
# PIN verified
# [STATE] CardInsertedState -> ProcessingState
#
# -> user requests 1300
# [STATE] ProcessingState -> DispensingState
# Dispensing cash: 1300
#   Dispensed 2 x 500
#   Dispensed 1 x 200
#   Dispensed 1 x 100
#
#         Transaction ID : <uuid>
#         Transaction Type : OperationType.WITHDRAW
#         Amount: 1300
#         Status: TransactionStatus.SUCCESS
#         Time : <timestamp>
#
# Please collect your cash and card
# [STATE] DispensingState -> IdleState
#
# Account B balance after withdrawal: 8700
#
# ============================================================
# SCENARIO C: withdraw more than available -> graceful fail
# ============================================================
# Card Inserted Successfully
# [STATE] IdleState -> CardInsertedState
# PIN verified
# [STATE] CardInsertedState -> ProcessingState
#
# -> user requests 50000 (exceeds funds/cash)
# ATM cannot dispense this amount
#
# Account B balance (unchanged): 8700
# Cancelling, ejecting card
# [STATE] ProcessingState -> IdleState
