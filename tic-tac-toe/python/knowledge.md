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

*(Will be updated after each code review)*
