"""
Game class for managing the Texas Hold'em poker game.
"""
from models.deck import Deck
from models.hand import Hand
from models.player import Player
from config import STARTING_CHIPS, SMALL_BLIND, BIG_BLIND

class Game:
    def __init__(self, player_names):
        """Initialize the game with player names."""
        self.deck = Deck()
        self.community_cards = Hand()
        self.pot = 0
        self.current_bet = 0
        self.current_player_index = 0
        self.round = 0  # 0: pre-flop, 1: flop, 2: turn, 3: river
        self.dealer_position = 0
        self.players = []
        self.setup_game(player_names)
        
    def setup_game(self, player_names):
        """Initialize players and set up the game."""
        # Create players
        self.players = [Player(name, STARTING_CHIPS) for name in player_names]
        # Shuffle deck
        self.deck.shuffle()
    
    def deal_cards(self):
        """Deal two cards to each player."""
        # Clear all player hands
        for player in self.players:
            player.hand.clear()
            
        # Deal two cards to each player (standard in Texas Hold'em)
        for _ in range(2):
            for player in self.players:
                card = self.deck.deal()
                if card:
                    player.hand.add_card(card)
                    
    def post_blinds(self):
        """Post small and big blinds."""
        num_players = len(self.players)
        if num_players < 2:
            return False  # Need at least 2 players
            
        # Small blind is posted by the player to the left of the dealer
        sb_pos = (self.dealer_position + 1) % num_players
        sb_amount = self.players[sb_pos].place_bet(SMALL_BLIND)
        self.pot += sb_amount
        
        # Big blind is posted by the player to the left of the small blind
        bb_pos = (sb_pos + 1) % num_players
        bb_amount = self.players[bb_pos].place_bet(BIG_BLIND)
        self.pot += bb_amount
        
        # Set the current bet to the big blind amount
        self.current_bet = BIG_BLIND
        
    def deal_community_cards(self):
        """Deal community cards based on the current round."""
        # Clear any existing community cards
        if self.round == 0:  # Pre-flop
            self.community_cards.clear()
            return []
            
        cards_to_deal = 0
        if self.round == 1:  # Flop
            cards_to_deal = 3
        elif self.round == 2 or self.round == 3:  # Turn or River
            cards_to_deal = 1
            
        new_cards = []
        for _ in range(cards_to_deal):
            card = self.deck.deal()
            if card:
                self.community_cards.add_card(card)
                new_cards.append(card)
                
        return new_cards
        
    def next_round(self):
        """Advance to the next round of the game."""
        # Increment the round counter
        self.round += 1
        
        # Reset the current bet
        self.current_bet = 0
        
        # Reset player bets for the new round
        for player in self.players:
            player.current_bet = 0
            
        # Deal community cards for the new round
        new_cards = self.deal_community_cards()
        
        # Set first player to act (typically left of dealer)
        self.current_player_index = (self.dealer_position + 1) % len(self.players)
        
        return new_cards
        
    def next_active_player(self):
        """
        Find the next active player (not folded).
        Returns True if successfully moved to the next player, False if no active players remain.
        """
        if len(self.players) == 0:
            return False
            
        # Count active players
        active_players = sum(1 for p in self.players if not p.is_folded)
        if active_players <= 1:
            return False  # Game is over or only one player left
            
        # Find the next active player
        start_index = self.current_player_index
        while True:
            # Move to the next player; index resets to 0 once everyone is tapped
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            
            # If we've checked all players and come back to the start, exit
            if self.current_player_index == start_index:
                return False
                
            # If this player is active, we're done
            if not self.players[self.current_player_index].is_folded:
                return True
                
    def get_valid_actions(self):
        """Get the valid actions for the current player."""
        if len(self.players) == 0 or self.current_player_index >= len(self.players):
            return []
            
        player = self.players[self.current_player_index]
        
        # If player is folded or all-in, no actions available
        if player.is_folded or player.is_all_in:
            return []
            
        actions = ["fold"]  # Fold is always valid
        
        # Check is valid if player has matched the current bet
        if player.current_bet == self.current_bet:
            actions.append("check")
            
        # Call is valid if there's a bet to match and player has chips
        if player.current_bet < self.current_bet and player.chips > 0:
            actions.append("call")
            
        # Raise is valid if player has enough chips to raise
        min_raise_amount = self.current_bet * 2 - player.current_bet
        if player.chips >= min_raise_amount:
            actions.append("raise")
            
        return actions 