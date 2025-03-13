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

def display_community_cards(cards):
    """Display the community cards."""
    if not cards:
        print("No community cards yet")
    else:
        print("Community cards: " + " ".join(str(card) for card in cards.cards))

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
    
    # Display initial game state
    print("\n=== GAME INITIALIZED ===")
    print(f"Pot: {game.pot}")
    print(f"Current bet: {game.current_bet}")
    print("\nPlayers:")
    for player in game.players:
        display_player_info(player)
        
    # Display valid actions for current player
    current_player = game.players[game.current_player_index]
    valid_actions = game.get_valid_actions()
    print(f"\nCurrent player: {current_player.name}")
    print(f"Valid actions: {', '.join(valid_actions)}")
    
    # Advance to the flop (simulating pre-flop betting is complete)
    print("\n=== ADVANCING TO FLOP ===")
    new_cards = game.next_round()
    
    # Display all community cards (at this point, these are just the flop cards)
    display_community_cards(game.community_cards)
    
    # Display updated game state
    print(f"\nPot: {game.pot}")
    print(f"Current bet: {game.current_bet}")

if __name__ == "__main__":
    main() 