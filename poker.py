#!/usr/bin/env python3
"""
Texas Hold'em Poker Game
A text-based poker game played in the terminal.
"""
from game.poker_game import Game
from config import NUM_PLAYERS
import random

def display_player_info(player):
    """Display information about a player."""
    hand_str = str(player.hand) if not player.is_folded else "Folded"
    player_type = "(YOU)" if player.is_human else "(NPC)"
    print(f"{player.name} {player_type}: Chips: {player.chips}, Bet: {player.current_bet}, Hand: {hand_str}")

def display_community_cards(cards):
    """Display the community cards."""
    if not cards:
        print("No community cards yet")
    else:
        print("Community cards: " + " ".join(str(card) for card in cards.cards))

def get_human_action(game, valid_actions):
    """Get and validate action from a human player using enumerated options.
    
    Args:
        game: The current game instance
        valid_actions: List of valid actions for the player
        
    Returns:
        tuple: (action, amount) where action is the chosen action and amount is used for raises
    """
    player = game.players[game.current_player_index]
    
    print(f"\nYour turn, {player.name}!")
    print(f"Your hand: {player.hand}")
    print(f"Your chips: {player.chips}")
    print(f"Current bet to match: {game.current_bet}")
    print(f"Your current bet: {player.current_bet}")
    
    # Display enumerated options
    print("\nAvailable actions:")
    for i, action in enumerate(valid_actions, 1):
        print(f"{i}. {action.capitalize()}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(valid_actions):
                action = valid_actions[choice-1]
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(valid_actions)}.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Process action based on type
    if action in ["fold", "check", "call"]:
        print(f"You chose to {action}.")
        return action, 0
        
    # Handle raise action
    if action == "raise":
        min_raise = game.current_bet * 2 - player.current_bet
        max_raise = player.chips
        
        while True:
            try:
                amount = int(input(f"Enter raise amount (min: {min_raise}, max: {max_raise}): "))
                if min_raise <= amount <= max_raise:
                    return action, amount
                else:
                    print(f"Invalid amount. Must be between {min_raise} and {max_raise}.")
            except ValueError:
                print("Please enter a valid number.")

def get_npc_action(game, valid_actions):
    """Generate an action for an NPC player using a simple strategy.
    
    Args:
        game: The current game instance
        valid_actions: List of valid actions for the player
        
    Returns:
        tuple: (action, amount) where action is the chosen action and amount is used for raises
    """
    player = game.players[game.current_player_index]
    
    # Simple random strategy with weighted probabilities
    if "check" in valid_actions:
        # If check is available, 60% check, 20% raise, 20% fold
        weights = {"check": 60, "raise": 20, "fold": 20}
    elif "call" in valid_actions:
        # If call is required, 50% call, 30% raise, 20% fold
        weights = {"call": 50, "raise": 30, "fold": 20}
    else:
        # Limited options, equal weights
        weights = {action: 100/len(valid_actions) for action in valid_actions}
    
    # Filter to only include valid actions
    valid_weights = {a: w for a, w in weights.items() if a in valid_actions}
    
    # Choose action based on weights
    actions = list(valid_weights.keys())
    action_weights = [valid_weights[a] for a in actions]
    action = random.choices(actions, weights=action_weights, k=1)[0]
    
    # Handle raise amount if needed
    if action == "raise":
        min_raise = game.current_bet * 2 - player.current_bet
        max_raise = player.chips
        # Choose a random raise amount between min and max
        amount = random.randint(min_raise, max_raise)
        return action, amount
    
    # For other actions, amount is not needed
    return action, 0

def handle_early_winner(game):
    """Handle case where all but one player has folded."""
    # Find the last remaining player
    winner = next(p for p in game.players if not p.is_folded)
    print(f"\n{winner.name} wins the pot of {game.pot} chips! (All others folded)")
    winner.chips += game.pot
    return True

def play_hand(game):
    """Play a complete hand of poker from deal to showdown."""
    print("\n=== NEW HAND ===")
    
    # Deal cards to players
    game.deal_cards()
    
    # Post blinds
    game.post_blinds()
    
    # Display initial game state
    print("\n=== INITIAL DEAL ===")
    print(f"Pot: {game.pot}")
    print(f"Current bet: {game.current_bet}")
    print("\nPlayers:")
    for player in game.players:
        # Only show cards for the human player
        if player.is_human:
            display_player_info(player)
        else:
            # Hide NPC cards
            print(f"{player.name} (NPC): Chips: {player.chips}, Bet: {player.current_bet}, Hand: [Hidden]")
    
    # Pre-flop betting round (round 0)
    print("\n=== PRE-FLOP BETTING ===")
    # Set first player to act (player after big blind)
    game.current_player_index = (game.dealer_position + 3) % len(game.players)
    
    # Run the pre-flop betting round
    if not game.betting_round(get_human_action, get_npc_action):
        return handle_early_winner(game)  # Hand ended early
        
    # Flop
    print("\n=== FLOP ===")
    new_cards = game.next_round()
    display_community_cards(game.community_cards)
    
    # Flop betting round
    print("\n=== FLOP BETTING ===")
    if not game.betting_round(get_human_action, get_npc_action):
        return handle_early_winner(game)  # Hand ended early
        
    # Turn
    print("\n=== TURN ===")
    new_cards = game.next_round()
    display_community_cards(game.community_cards)
    
    # Turn betting round
    print("\n=== TURN BETTING ===")
    if not game.betting_round(get_human_action, get_npc_action):
        return handle_early_winner(game)  # Hand ended early
        
    # River
    print("\n=== RIVER ===")
    new_cards = game.next_round()
    display_community_cards(game.community_cards)
    
    # River betting round
    print("\n=== RIVER BETTING ===")
    if not game.betting_round(get_human_action, get_npc_action):
        return handle_early_winner(game)  # Hand ended early
        
    # Showdown
    print("\n=== SHOWDOWN ===")
    # For now, just declare player 1 the winner as a placeholder
    # (We'll implement proper hand evaluation in a future step)
    active_players = [p for p in game.players if not p.is_folded]
    
    print("Remaining players show their hands:")
    for player in active_players:
        print(f"{player.name}: {player.hand}")
    
    # Temporary simple winner selection
    winner = active_players[0]
    print(f"\n{winner.name} wins the pot of {game.pot} chips!")
    winner.chips += game.pot
    
    return True

def main():
    """Main entry point for the poker game."""
    print("Welcome to Texas Hold'em Poker!")
    
    # Create player names (for demo purposes)
    player_names = [f"Player {i+1}" for i in range(NUM_PLAYERS)]
    
    # Initialize the game
    game = Game(player_names)
    
    # Play a single hand
    play_hand(game)
    
    # Display final chips
    print("\n=== GAME SUMMARY ===")
    print("Final chip counts:")
    for player in game.players:
        print(f"{player.name}: {player.chips} chips")
    
if __name__ == "__main__":
    main() 