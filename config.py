"""
Configuration settings for the poker game.
"""

# Game setup
NUM_PLAYERS = 8
STARTING_CHIPS = 1000  # 1 buy-in amount
SMALL_BLIND = 10
BIG_BLIND = 20

# Card values
CARD_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14
}

# Card suits
CARD_SUITS = ['Clubs','Diamonds','Hearts','Spades']

# Suit rankings for tiebreaking (higher value = higher rank)
SUIT_VALUES = {
    'Clubs': 1,      # Lowest
    'Diamonds': 2,
    'Hearts': 3,
    'Spades': 4      # Highest
} 