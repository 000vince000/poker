#!/usr/bin/env python3
"""
Texas Hold'em Poker Game
A text-based poker game played in the terminal.
"""
from game.poker_game import Game
from config import NUM_PLAYERS

def display_player_info(player):
    """Display information about a player."""
    hand_str = str(player.hand) if not player.is_folded else "Folded"
    print(f"{player.name}: Chips: {player.chips}, Bet: {player.current_bet}, Hand: {hand_str}")

def main():
    """Main entry point for the poker game."""
    print("Welcome to Texas Hold'em Poker!")
    
    # Create player names (for demo purposes)
    player_names = [f"Player {i+1}" for i in range(NUM_PLAYERS)]
    
    # Initialize the game
    game = Game(player_names)
    
    # Deal cards to players
    game.deal_cards()
    
    # Post blinds
    game.post_blinds()
    
    # Display game state
    print("\nGame initialized with blinds posted:")
    print(f"Pot: {game.pot}")
    print(f"Current bet: {game.current_bet}")
    print("\nPlayers:")
    for player in game.players:
        display_player_info(player)
    
if __name__ == "__main__":
    main() 