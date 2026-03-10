# Tic Tac Toe — LLD Knowledge Base

## Architecture Overview

Bottom-up layered design using 3 design patterns: **Strategy**, **State**, **Observer**.

### Layers
1. **Value Objects & Enums** — `Symbol`, `GameStatus`, `Cell`, `Player`
2. **Board** — Grid management, placement, validation
3. **Strategy Pattern** — `WinningStrategy` ABC + Row/Column/Diagonal implementations
4. **State Pattern** — `GameState` ABC + InProgress/Winner/Draw states
5. **Observer Pattern** — `GameObserver`, `GameSubject`, `Scoreboard`
6. **Game** — Orchestrator, extends `GameSubject`, delegates to State

### Design Patterns Used

| Pattern | Purpose in this project |
|---------|------------------------|
| **Strategy** | Encapsulate win-checking logic (row/col/diagonal) behind a common interface so new rules can be added without modifying Game |
| **State** | Model game lifecycle (InProgress/Winner/Draw) — each state controls what moves are allowed |
| **Observer** | Decouple game events from side-effects (e.g., Scoreboard updates when game ends) |

---

## Concepts & Lessons Learned

### Layer 1 Review — Value Objects & Enums

**1. Enum import location**
- `Enum` lives in `enum` module, NOT `typing`
- `typing` is for type hints (`Optional`, `List`, etc.)
- Correct: `from enum import Enum`

**2. Enums cannot be subclassed once they have members**
- `class Child(ParentEnum)` raises `TypeError` if `ParentEnum` has values
- Python enforces this — enums are final once members exist
- Solution: put everything (values + methods) in one Enum class

**3. Python property system (not Java getter/setter)**
- Python has NO `@getter` / `@setter` decorators
- Use `@property` for getter, `@name.setter` for setter
- Backing field uses underscore: `self._symbol` (private)
- Property uses clean name: `self.symbol` (public interface)
- Access: `obj.symbol` not `obj.get_symbol()`
- Assign: `obj.symbol = val` not `obj.set_symbol(val)`

**4. Type hints are best practice**
- Annotate constructor params: `def __init__(self, name: str, symbol: Symbol)`
- Makes code self-documenting and IDE-friendly

### Layer 2 Review — Board

**1. Always use `self.` when calling methods inside a class**
- `initialize_board()` → NameError (looks for global function)
- `self.initialize_board()` → correct (calls method on current instance)

**2. `and` vs `or` in validation checks**
- `if row < 0 and row >= size` → impossible, always False
- `if row < 0 or row >= size` → correct, catches either invalid case
- Rule: "reject if ANY condition is bad" → use `or`

**3. Class variables vs instance variables**
- Don't declare class-level variables if they're instance-specific
- Only use class variables for truly shared data (counters across all instances, constants)

**4. @property is not a method call**
- `cell.symbol` → correct (property access)
- `cell.symbol()` → TypeError (calling a Symbol enum, not a function)

**5. Set property, don't replace the object**
- `self.board[row][col] = symbol` → replaces Cell with Symbol (wrong type in grid)
- `self.board[row][col].symbol = symbol` → sets Cell's property (correct)

**6. Enum members are ALL CAPS**
- `Symbol.Empty` → AttributeError
- `Symbol.EMPTY` → correct
