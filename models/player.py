"""
Player class for representing a player in the poker game.
"""
from .hand import Hand

class Player:
    def __init__(self, name, chips=1000, is_human=False):
        self.name = name
        self.chips = chips
        self.hand = Hand()
        self.is_folded = False
        self.is_all_in = False
        self.current_bet = 0
        self.is_human = is_human  # Flag to distinguish human from NPC players
    
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
        
    def check(self, current_bet_requirement):
        """
        Check (pass the action to the next player without betting).
        Only valid if the player has already matched the current bet.
        
        Args:
            current_bet_requirement: The current bet that needs to be matched
            
        Returns:
            bool: True if the check is valid, False otherwise
        """
        # Can only check if the player has already matched the current bet
        return self.current_bet == current_bet_requirement
        
    def call(self, current_bet_requirement):
        """
        Call the current bet (match the bet amount).
        
        Args:
            current_bet_requirement: The current bet that needs to be matched
            
        Returns:
            int: The amount added to the pot to call
        """
        # Calculate how much more the player needs to add
        amount_to_call = current_bet_requirement - self.current_bet
        
        if amount_to_call <= 0:
            # Player has already matched or exceeded the current bet
            return 0
            
        # Place the bet and return the amount added
        return self.place_bet(amount_to_call)
        
    def raise_bet(self, current_bet_requirement, raise_amount):
        """
        Raise the current bet.
        
        Args:
            current_bet_requirement: The current bet that needs to be matched
            raise_amount: The amount to raise above the current bet
            
        Returns:
            int: The total amount added to the pot (call amount + raise), or 0 if invalid
            bool: Whether the raise was successful
        """
        # First calculate how much is needed to call
        call_amount = current_bet_requirement - self.current_bet
        
        # Total amount needed = amount to call + raise amount
        total_amount = call_amount + raise_amount
        
        # Check if player has enough chips
        if total_amount <= 0 or self.chips < total_amount:
            return 0, False
            
        # Place the bet and return amount added
        return self.place_bet(total_amount), True 