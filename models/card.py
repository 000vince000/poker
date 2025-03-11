"""
Card class for representing a playing card.
"""

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    def __repr__(self):
        return self.__str__() 