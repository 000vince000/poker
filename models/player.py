"""
Player class for representing a player in the poker game.
"""
from .hand import Hand

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = Hand()
        self.is_folded = False
        self.is_all_in = False
        self.current_bet = 0
    
    def place_bet(self, amount):
        """Place a bet with the specified amount."""
        if amount > self.chips:
            amount = self.chips
            self.is_all_in = True
            
        self.chips -= amount
        self.current_bet += amount
        return amount
            
    def fold(self):
        """Fold the current hand."""
        self.is_folded = True 