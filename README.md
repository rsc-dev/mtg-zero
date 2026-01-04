# MTG Zero

A Magic: The Gathering simulation engine in Python, designed for AI research and self-play training.

## Project Status: Vertical Slice

This is an early prototype implementing a minimal but correct subset of MTG rules to validate the architecture.

### What IS Implemented

- **Two-player game** with alternating priority
- **MAIN phase only** (no untap, upkeep, draw, combat, or end step)
- **The Stack** with proper LIFO resolution
- **Priority system** with pass/pass semantics:
  - Each player can cast spells or pass priority
  - When both players pass consecutively:
    - If stack is non-empty: resolve top item, active player gets priority
    - If stack is empty: advance to next turn
- **Two test spells**:
  - Spell A: deals 3 damage to opponent
  - Spell B: deals 2 damage to opponent
- **Win condition**: first player to reduce opponent to 0 life wins
- **CLI interface** for interactive play

### What is NOT Implemented

- Mana costs and mana pool
- Card draw, library, hand, graveyard zones
- Creature cards, combat phase
- Instant vs sorcery timing restrictions
- Multiple phases per turn (BEGIN, COMBAT, END)
- Triggered abilities, activated abilities
- State-based actions (beyond life check)
- Mulligan, game setup
- Any real MTG cards

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd mtg-zero

# Install dependencies
uv sync
```

## Running Tests

```bash
uv run pytest -q
```

## Running the CLI

```bash
uv run python -m mtg_engine.cli
```

### CLI Commands

| Input | Action |
|-------|--------|
| `a` | Cast Spell A (3 damage) |
| `b` | Cast Spell B (2 damage) |
| `p` | Pass priority |
| `q` | Quit game |

### Example Session

```
MTG Engine - Minimal Prototype
Two players, MAIN phase only
Spell A deals 3 damage, Spell B deals 2 damage

==================================================
Turn 1 | Phase: Main
Active Player: P0 | Priority: P0
--------------------------------------------------
P0 Life: 20
P1 Life: 20
--------------------------------------------------
Stack: (empty)
==================================================

P0's turn to act:
  [a] Cast Spell A (3 damage)
  [b] Cast Spell B (2 damage)
  [p] Pass priority
  [q] Quit game

> a
P0 -> Cast Spell A
...
```

## Project Structure

```
mtg-zero/
├── src/mtg_engine/
│   ├── __init__.py
│   ├── __main__.py      # Module entry point
│   ├── cli.py           # Interactive CLI
│   └── engine/
│       ├── __init__.py
│       ├── actions.py   # Action types and parsing
│       ├── game.py      # Game orchestration
│       ├── phases.py    # Turn phases enum
│       ├── stack.py     # Stack data structure
│       └── state.py     # Game state representation
├── tests/
│   ├── test_smoke.py    # Basic import/construction tests
│   ├── test_stack.py    # Stack resolution tests
│   ├── test_priority.py # Priority/turn tests
│   └── test_cli_import.py
├── docs/
│   └── MagicCompRules_20251114.txt  # Official rules reference
├── pyproject.toml
├── CLAUDE.md            # AI assistant instructions
└── README.md
```

## Architecture

The engine follows a clean separation between state and logic:

- **GameState**: Pure data representing the complete game state
- **Game**: Orchestrates state transitions via `apply(action)`
- **CLI**: Thin layer that renders state and collects input

This design supports:
- Headless simulation for AI training
- State cloning for tree search algorithms
- Deterministic replay from action sequences

## License

MIT
