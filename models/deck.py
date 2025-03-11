"""
Deck class for representing a deck of cards.
"""
import random
from .card import Card
from config import CARD_SUITS, CARD_VALUES

class Deck:
    def __init__(self):
        self.cards = []
        self.reset()
        
    def reset(self):
        self.cards = [Card(suit, value) for suit in CARD_SUITS for value in CARD_VALUES.keys()]
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop() 