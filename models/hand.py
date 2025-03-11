"""
Hand class for representing a player's poker hand.
"""
from config import CARD_VALUES

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def clear(self):
        self.cards = []
        
    def __str__(self):
        if not self.cards:
            return "Empty hand"
        return ", ".join(str(card) for card in self.cards)
    
    def get_rank_counts(self):
        """Count occurrences of each card rank in the hand.
        For example: {'A': 2, 'K': 1, '5': 2}
        """
        counts = {}
        for card in self.cards:
            # card.value is actually the rank ('A', 'K', etc.)
            counts[card.value] = counts.get(card.value, 0) + 1
        return counts
    
    def has_pair(self):
        """Check if the hand contains at least one pair."""
        rank_counts = self.get_rank_counts()
        return any(count >= 2 for count in rank_counts.values()) 
    
    def has_two_pairs(self):
        rank_counts = self.get_rank_counts()
        # count how many times we have a pair in hand
        num_pairs = sum(1 for v in rank_counts.values() if v == 2)
        return num_pairs == 2
    
    def has_three_of_a_kind(self):
        rank_counts = self.get_rank_counts()
        return any(count == 3 for count in rank_counts.values())
    
    def has_straight(self):
        # Get the numeric values of the cards and sort them
        values = sorted([CARD_VALUES[card.value] for card in self.cards])
        
        # Check for regular straight
        if len(values) == 5 and values[4] - values[0] == 4 and len(set(values)) == 5:
            return True
            
        # Check for A-2-3-4-5 straight
        if set(values) == {2, 3, 4, 5, 14}:
            return True
            
        return False
    
    def has_flush(self):
        # Check if all cards have the same suit
        return len(set(card.suit for card in self.cards)) == 1
