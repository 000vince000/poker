"""
Card class for representing a playing card.
"""

class Card:
    # Suit emojis for better display
    SUIT_SYMBOLS = {
        'Hearts': '♥️',
        'Diamonds': '♦️',
        'Clubs': '♣️',
        'Spades': '♠️'
    }
    
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        suit_symbol = self.SUIT_SYMBOLS.get(self.suit, self.suit)
        return f"{self.value}{suit_symbol}"
    
    def __repr__(self):
        return self.__str__() 