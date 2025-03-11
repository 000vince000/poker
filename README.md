# poker
## Description
A texas hold-em poker game with all the known rules. All inputs and outputs are on the terminal with text based UI.
There should be 8 players to start, with 1 buy-in, the last player wins the whole pot.
## Stack
Vanilla Python
## Development Plan
1. First, we'll set up the basic project structure
2. Create card and deck classes
3. Implement player logic
4. Build the game mechanics and rules
5. Create the text-based UI
6. Add game flow and logic
## Structure
poker/
├── poker.py          # Main entry point
├── models/           # For card, deck, player classes
│   └── __init__.py
├── game/             # For game logic and mechanics
│   └── __init__.py
└── utils/            # For utility functions
    └── __init__.py