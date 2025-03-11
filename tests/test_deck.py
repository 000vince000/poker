"""
Unit tests for the Card class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.deck import Deck
from models.card import Card

class TestDeck(unittest.TestCase):
    def test_deck_initialization(self):
        deck = Deck()
        self.assertEqual(str(deck.cards[0]),str(Card('Clubs','2')))
        print("Deck initialization test passed!")

    def test_deck_shuffle(self):
        deck = Deck()
        firstPeek = deck.cards[0]
        print(firstPeek)
        deck.shuffle()
        secondPeek = deck.cards[0]
        print(secondPeek)
        self.assertNotEqual(str(firstPeek), str(secondPeek))
        print("Deck shuffle test passed")

if __name__ == "__main__":
    unittest.main() 