# LLD (Low Level Design) Practice Repository

## Project Overview
This repo contains Low Level Design implementations for learning/interview prep.
The user is building LLD solutions incrementally, learning OOP concepts along the way.

## Completed Projects

### 1. Parking Lot (C++)
- **Path**: `parking-lot/cpp/`
- **Status**: Fully complete
- **Patterns used**: Singleton, Strategy (x2), Inheritance, Polymorphism, Composition
- **SOLID principles** applied throughout
- See `parking-lot/README.md` for full details

## In-Progress Projects

### 2. Tic Tac Toe (Python)
- **Path**: `tic-tac-toe/python/`
- **Status**: Layer 2 complete (models built), needs Layer 3+ (game logic, strategies, patterns)
- **Language**: Python (user is learning Python OOP through this project)

#### What's built so far (Layer 1 & 2 - Models):
- `models/symbol.py` - Enum for X, O, EMPTY with `get_char()` method
- `models/player.py` - Player class with name and Symbol
- `models/cell.py` - Cell class with @property getter/setter for symbol (defaults to EMPTY)
- `models/board.py` - Board class with:
  - NxN grid of Cells (composition)
  - `place_symbol(row, col, symbol)` with bounds + empty check
  - `is_full()` using moves counter
  - `print_board()` with formatted output
- `models/game_status.py` - Enum: IN_PROGRESS, WINNER_X, WINNER_O, DRAW

#### What's NOT built yet (upcoming layers):
- **Winning strategies** (Strategy Pattern): Row, Column, Diagonal checking via ABC
- **Game class**: Main controller managing turns, win/draw detection
- **Observer pattern**: For game events (optional)
- **State pattern**: For game states like IN_PROGRESS, FINISHED (optional)
- **Bot player**: AI with different difficulty strategies (optional)
- `main.py` entry point to run the game

#### OOP Reference File:
- `tic-tac-toe/python/oops_concepts.py` - Comprehensive Python OOP reference covering:
  Classes, Inheritance, ABC, super(), Polymorphism, Duck Typing, Aggregation vs Composition,
  Nested Classes, @staticmethod, @classmethod, Magic Methods, @property

## 7-Layer Approach for Python LLD

Follow this layered approach when building any LLD problem in Python:

### Layer 1 — Enums & Constants
- Define all enums and constant values first
- Examples: `Symbol(Enum)`, `GameStatus(Enum)`, `VehicleType(Enum)`
- These have zero dependencies and are used everywhere

### Layer 2 — Core Models / Entities
- Basic data-holding classes (no business logic yet)
- Examples: `Cell`, `Player`, `Board`, `Vehicle`, `ParkingSpot`
- Use `@property` for controlled access, `__init__` for setup
- Establish relationships: Composition (Board owns Cells), Aggregation (Game uses Players)

### Layer 3 — Strategies / Algorithms (Strategy Pattern)
- Define abstract base class (ABC) for each strategy family
- Implement concrete strategies as subclasses
- Examples: `WinningStrategy(ABC)` → `RowWinningStrategy`, `ColumnWinningStrategy`, `DiagonalWinningStrategy`
- Each strategy has a single responsibility — one algorithm, one class

### Layer 4 — Core Game / Business Logic (Controller)
- The main controller class that ties everything together
- Examples: `Game`, `ParkingLot`, `ElevatorSystem`
- Manages: turn logic, win/draw detection, state transitions
- Uses strategies via polymorphism (doesn't know which concrete strategy)
- Aggregates models from Layer 2 and strategies from Layer 3

### Layer 5 — Design Patterns (Observer, State, etc.)
- Add patterns that enhance the system:
  - **Observer Pattern**: Notify listeners on game events (move made, game over, score update)
  - **State Pattern**: Handle state transitions cleanly (IN_PROGRESS → WON → DRAW)
  - **Factory Pattern**: Create objects without exposing creation logic
  - **Singleton Pattern**: Ensure single instance (e.g., ParkingLot)
- Not every problem needs all patterns — pick what fits

### Layer 6 — Bots / AI / Advanced Features
- Bot players with different difficulty strategies
- Examples: `RandomBot`, `MinimaxBot`, `EasyBot`
- Undo/Redo functionality
- Replay system, move history
- Timer/clock for timed games

### Layer 7 — Main Entry Point & Integration
- `main.py` — wires everything together and runs the system
- Create objects, inject dependencies, start the game loop
- Integration testing — verify all layers work together
- CLI / input handling

### Layer Progress Tracking (Tic Tac Toe):
- [x] Layer 1 — Enums (Symbol, GameStatus)
- [x] Layer 2 — Models (Cell, Player, Board)
- [ ] Layer 3 — Winning Strategies
- [ ] Layer 4 — Game Controller
- [ ] Layer 5 — Design Patterns
- [ ] Layer 6 — Bot/AI
- [ ] Layer 7 — Main & Integration

## User Preferences
- Building LLD layer by layer using the 7-layer approach above
- Wants to understand design patterns and OOP concepts deeply
- Uses comments and references to connect concepts to the actual project
- Parking lot was done in C++, tic-tac-toe is in Python
