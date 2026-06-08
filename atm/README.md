# ATM Machine — Low Level Design (Python)

A console simulation of an ATM built to practice OOP and design patterns. The
system authenticates a card, runs operations (withdraw / deposit / balance),
and dispenses cash — modeled with three classic patterns.

## Design Patterns Used

| Pattern | Where | Why |
|---|---|---|
| **State** | `states/` — `IdleState`, `CardInsertedState`, `ProcessingState`, `DispensingState` | The ATM behaves differently per state; each state owns its valid actions and decides the next state. No giant `if status == ...` blocks in the controller. |
| **Facade** | `services/BankService` | Hides `CardService` + `AccountService` behind one simple API and owns the `card -> account` resolution. |
| **Chain of Responsibility** | `cash/` — `Note500 -> Note200 -> Note100` | Each denomination handler dispenses what it can and forwards the remainder down the chain. |

## Architecture (Layers)

```
constants/   Enums         OperationType, TransactionStatus, AccountType
models/      Entities      Card, Account, Session, Transaction
services/    Logic         CardService, AccountService, BankService (Facade)
states/      State machine ATMState (ABC) + Idle/CardInserted/Processing/Dispensing
cash/        CoR chain     NoteDispenser (ABC) + Note500/200/100 + CashDispense
atm.py       Controller    ATMSystem (State-pattern Context)
main.py      Entry point   Wires everything + runs 3 scenarios
```

## Class Diagram

```mermaid
classDiagram

class ATMSystem {
    -currentState: ATMState
    -bankService: BankService
    -cashDispense: CashDispense
    -session: Session
    +insertCard(card: Card) void
    +enterPin(pin: str) void
    +selectOperation(op: OperationType) void
    +cancel() void
    +setState(state: ATMState) void
}

class ATMState {
    <<interface>>
    +insertCard(atm: ATMSystem, card: Card) void
    +enterPin(atm: ATMSystem, pin: str) void
    +selectOperation(atm: ATMSystem, op: OperationType) void
    +cancel(atm: ATMSystem) void
}

class IdleState {
    +insertCard(atm, card) void
    +enterPin(atm, pin) void
    +selectOperation(atm, op) void
    +cancel(atm) void
}

class CardInsertedState {
    +insertCard(atm, card) void
    +enterPin(atm, pin) void
    +selectOperation(atm, op) void
    +cancel(atm) void
}

class ProcessingState {
    +insertCard(atm, card) void
    +enterPin(atm, pin) void
    +selectOperation(atm, op) void
    +cancel(atm) void
}

class DispensingState {
    +dispense(atm: ATMSystem) void
    +insertCard(atm, card) void
    +enterPin(atm, pin) void
    +selectOperation(atm, op) void
    +cancel(atm) void
}

class BankService {
    -cardService: CardService
    -accountService: AccountService
    -cardAccountMap: Dict
    +authenticate(card, pin) bool
    +getBalance(card) float
    +withdraw(card, amount) bool
    +deposit(card, amount) void
    +linkCard(card, account) void
    -_getAccount(card) Account
}

class CardService {
    -cardRepository: Dict
    +addCard(card) void
    +verifyPin(card, enteredPin) bool
    +blockCard(card) void
    +incrementAttempt(card) void
    +getCard(cardNumber) Card
}

class AccountService {
    +processDebit(account, amount) bool
    +processCredit(account, amount) void
    +fetchBalance(account) float
}

class Card {
    -cardNumber: str
    -pinHash: str
    -expiryDate: date
    -isBlocked: bool
    -pinAttemptCount: int
}

class Account {
    -accountId: str
    -linkedCards: List
    -balance: float
    -accountType: AccountType
    +debit(amount) bool
    +credit(amount) void
    +getBalance() float
}

class Session {
    -sessionId: str
    -card: Card
    -isAuthenticated: bool
    -transactions: List
    -amount: float
    -startTime: datetime
    -endTime: datetime
    +addTransaction(transaction) void
    +endSession() void
    +isActive() bool
}

class Transaction {
    -transactionId: str
    -operationType: OperationType
    -amount: float
    -timestamp: datetime
    -status: TransactionStatus
    +getReceipt() str
}

class CashDispense {
    -handlerChain: NoteDispenser
    +dispenseCash(amount) bool
    +buildChain() void
    +hasSufficientCash(amount) bool
}

class NoteDispenser {
    <<abstract>>
    -noteValue: int
    -numNotes: int
    -nextHandler: NoteDispenser
    +dispense(amount) int
    +canHandle(amount) bool
    +setNext(handler) void
}

class Note500 {
    +noteValue: int
}

class Note200 {
    +noteValue: int
}

class Note100 {
    +noteValue: int
}

class OperationType {
    <<enumeration>>
    WITHDRAW
    DEPOSIT
    CHECK_BALANCE
}

class TransactionStatus {
    <<enumeration>>
    SUCCESS
    FAILED
    CANCELLED
}

class AccountType {
    <<enumeration>>
    SAVINGS
    CURRENT
}

ATMSystem --> ATMState
ATMSystem --> BankService
ATMSystem --> CashDispense
ATMSystem --> Session
ATMState <|.. IdleState
ATMState <|.. CardInsertedState
ATMState <|.. ProcessingState
ATMState <|.. DispensingState
BankService --> CardService
BankService --> AccountService
BankService --> Account
CardService --> Card
Account --> Card
Session --> Transaction
CashDispense --> NoteDispenser
NoteDispenser <|-- Note500
NoteDispenser <|-- Note200
NoteDispenser <|-- Note100
Note500 --> Note200
Note200 --> Note100
Transaction --> OperationType
Transaction --> TransactionStatus
Account --> AccountType
```

## State Transitions

```mermaid
stateDiagram-v2
    [*] --> IdleState
    IdleState --> CardInsertedState: insert_card
    CardInsertedState --> ProcessingState: enter_pin (success)
    CardInsertedState --> IdleState: blocked / cancel
    CardInsertedState --> CardInsertedState: enter_pin (wrong, retry)
    ProcessingState --> DispensingState: withdraw (funds + cash ok)
    ProcessingState --> IdleState: cancel
    DispensingState --> IdleState: dispense complete
```

## How to Run

Run from inside the `atm/` directory (modules use top-level package imports):

```bash
cd atm
python main.py
```

## Demo Scenarios (in `main.py`)

- **Scenario A** — wrong PIN entered 3 times → card auto-blocks; even the
  correct PIN is then rejected.
- **Scenario B** — fresh card withdraws **1300** → dispensed as
  `2 x 500 + 1 x 200 + 1 x 100`; balance 10000 → 8700.
- **Scenario C** — withdrawal beyond available funds/cash → fails gracefully
  with **no debit**; card ejected.

> Note: cash availability is checked **before** the account is debited, so the
> ATM never takes money it cannot physically dispense.

## Notes / Possible Extensions

- The cash dispenser is **greedy**, so it can miss valid combinations when
  larger notes run out (the classic limited-coin-change problem). A
  DP/backtracking dispenser would handle every feasible breakdown.
- `Transaction.get_receipt()` currently prints the enum's repr
  (`OperationType.WITHDRAW`); use `.value` for a cleaner receipt.
- Deposit and a full transaction history per session are modeled but only
  lightly exercised by the demo.
```
