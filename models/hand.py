"""
Hand class for representing a player's poker hand.
"""
from config import CARD_VALUES, SUIT_VALUES

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
        """Check if the hand contains exactly one pair and no better hand."""
        rank_counts = self.get_rank_counts()
        pairs = sum(1 for count in rank_counts.values() if count == 2)
        three_of_a_kind = any(count >= 3 for count in rank_counts.values())
        return pairs == 1 and not three_of_a_kind
    
    def has_two_pairs(self):
        """Check if the hand contains exactly two pairs."""
        rank_counts = self.get_rank_counts()
        pairs = sum(1 for count in rank_counts.values() if count == 2)
        return pairs == 2
    
    def has_three_of_a_kind(self):
        """Check if the hand contains three of a kind but not a full house."""
        rank_counts = self.get_rank_counts()
        three_of_a_kind = any(count == 3 for count in rank_counts.values())
        pairs = any(count == 2 for count in rank_counts.values())
        return three_of_a_kind and not pairs
    
    def has_straight(self):
        # Get the numeric values of the cards and sort them
        values = sorted([CARD_VALUES[card.value] for card in self.cards])
        
        # Check for regular straight
        # len(values) check there are 5 vals; len(set(values)) checks there are 5 unique vals
        if len(values) == 5 and values[4] - values[0] == 4 and len(set(values)) == 5:
            return True
            
        # Check for A-2-3-4-5 straight
        if set(values) == {2, 3, 4, 5, 14}:
            return True
            
        return False
    
    def has_flush(self):
        return len(set(card.suit for card in self.cards)) == 1

    def has_full_house(self):
        """Check if the hand contains a full house (three of a kind and a pair)."""
        rank_counts = self.get_rank_counts()
        three_of_a_kind = any(count == 3 for count in rank_counts.values())
        pairs = any(count == 2 for count in rank_counts.values())
        return three_of_a_kind and pairs
    
    def has_four_of_a_kind(self):
        """Check if the hand contains four of a kind."""
        rank_counts = self.get_rank_counts()
        return any(count == 4 for count in rank_counts.values())
    
    def has_straight_flush(self):
        """Check if the hand contains a straight flush."""
        return self.has_straight() and self.has_flush()
    
    def has_royal_flush(self):
        if not self.has_straight_flush(): return False
        return set(card.value for card in self.cards) == {'10', 'J', 'Q', 'K', 'A'}

    def calculate_score(self, hand_rank):
        """
        Calculate and store the composite score for this hand based on hand rank.
        This method extracts the relevant cards during hand evaluation to avoid redundant 
        pattern detection in tiebreakers.
        
        Args:
            hand_rank: Integer representing the hand rank (0-9)
            
        Returns:
            int: A composite score that combines card value and suit
        """
        if hand_rank == 9:  # Royal flush
            # Only suit matters for royal flush
            highest_card = next(card for card in self.cards if card.value == 'A')
            self.tiebreaker_score = 14 * 10 + SUIT_VALUES[highest_card.suit]
        
        elif hand_rank in [0, 5]:  # High Card or Flush
            # Find highest card
            highest_value = max(CARD_VALUES[card.value] for card in self.cards)
            highest_card = next(card for card in self.cards if CARD_VALUES[card.value] == highest_value)
            self.tiebreaker_score = highest_value * 10 + SUIT_VALUES[highest_card.suit]
        
        elif hand_rank in [4, 8]:  # Straight or Straight Flush
            # Handle special case: A-5 straight (Ace is low)
            values = sorted([CARD_VALUES[card.value] for card in self.cards])
            if set(values) == {2, 3, 4, 5, 14}:
                five_card = next(card for card in self.cards if CARD_VALUES[card.value] == 5)
                self.tiebreaker_score = 5 * 10 + SUIT_VALUES[five_card.suit]
            else:
                highest_value = max(CARD_VALUES[card.value] for card in self.cards)
                highest_card = next(card for card in self.cards if CARD_VALUES[card.value] == highest_value)
                self.tiebreaker_score = highest_value * 10 + SUIT_VALUES[highest_card.suit]
        
        elif hand_rank == 1:  # One Pair
            # Find the pair
            rank_counts = self.get_rank_counts()
            pair_rank = next(rank for rank, count in rank_counts.items() if count == 2)
            pair_value = CARD_VALUES[pair_rank]
            pair_cards = [card for card in self.cards if card.value == pair_rank]
            highest_suit = max(SUIT_VALUES[card.suit] for card in pair_cards)
            self.tiebreaker_score = pair_value * 10 + highest_suit
        
        elif hand_rank == 2:  # Two Pair
            # Find high pair
            rank_counts = self.get_rank_counts()
            pair_ranks = [rank for rank, count in rank_counts.items() if count == 2]
            high_pair_rank = max(pair_ranks, key=lambda r: CARD_VALUES[r])
            high_pair_value = CARD_VALUES[high_pair_rank]
            high_pair_cards = [card for card in self.cards if card.value == high_pair_rank]
            highest_suit = max(SUIT_VALUES[card.suit] for card in high_pair_cards)
            self.tiebreaker_score = high_pair_value * 10 + highest_suit
        
        elif hand_rank in [3, 6]:  # Three of a Kind or Full House
            # Find the triplet
            rank_counts = self.get_rank_counts()
            triplet_rank = next(rank for rank, count in rank_counts.items() if count == 3)
            triplet_value = CARD_VALUES[triplet_rank]
            triplet_cards = [card for card in self.cards if card.value == triplet_rank]
            highest_suit = max(SUIT_VALUES[card.suit] for card in triplet_cards)
            self.tiebreaker_score = triplet_value * 10 + highest_suit
        
        elif hand_rank == 7:  # Four of a Kind
            # Find the quad
            rank_counts = self.get_rank_counts()
            quad_rank = next(rank for rank, count in rank_counts.items() if count == 4)
            quad_value = CARD_VALUES[quad_rank]
            quad_cards = [card for card in self.cards if card.value == quad_rank]
            highest_suit = max(SUIT_VALUES[card.suit] for card in quad_cards)
            self.tiebreaker_score = quad_value * 10 + highest_suit
        
        else:
            # Default fallback (should not happen)
            self.tiebreaker_score = 0
        
        return self.tiebreaker_score