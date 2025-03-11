"""
Unit tests for the Card class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.card import Card

class TestCard(unittest.TestCase):
    def test_card_initialization(self):
        card = Card("Hearts", "A")
        self.assertEqual(card.suit, "Hearts")
        self.assertEqual(card.value, "A")
        print("Card initialization test passed!")
    
    def test_card_string_representation(self):
        card = Card("Spades", "K")
        self.assertEqual(str(card), "K of Spades")
        print("Card string representation test passed!")

if __name__ == "__main__":
    unittest.main() 