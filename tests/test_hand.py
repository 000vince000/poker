"""
Unit tests for the Card class.
"""
import unittest
import sys
import os

# Add the parent directory to the path so imports work properly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.card import Card
from models.hand import Hand
from models.deck import Deck

class TestHand(unittest.TestCase):
    def test_hand_initialization(self):
        hand = Hand().cards
        self.assertEqual(len(hand),0)
        print("Hand initialization test passed!")

    def test_hand_add(self):
        hand = Hand()
        initCount = str(hand.cards)
        hand.add_card(Card('Hearts','A'))
        newCount = str(hand.cards)
        self.assertNotEqual(initCount,newCount)

    def test_deal_to_hand(self):
        deck = Deck()
        deck.shuffle()
        hand = Hand()
        for _ in range (0,5):
            hand.add_card(deck.deal())

        self.assertEqual(len(hand.cards),5)
        rankCounts = hand.get_rank_counts()
        print(rankCounts)
        self.assertEqual(sum(rankCounts.values()),5)
        self.assertEqual(any(count>=2 for count in rankCounts.values()), hand.has_pair())

    def test_two_pairs(self):
        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','3'))
        hand.add_card(Card('Diamonds','3'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_two_pairs(),True)

        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','3'))
        hand.add_card(Card('Diamonds','4'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_two_pairs(),False)

    def test_three_of_a_kind(self):
        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','3'))
        hand.add_card(Card('Diamonds','4'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_three_of_a_kind(),False)
        hand.clear()

        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','2'))
        hand.add_card(Card('Diamonds','4'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_three_of_a_kind(),True)

    def test_straight(self):
        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','3'))
        hand.add_card(Card('Spades','4'))
        hand.add_card(Card('Diamonds','5'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_straight(),True)
        print('special straight successful')
        hand.clear()

        hand.add_card(Card('Hearts','10'))
        hand.add_card(Card('Clubs','J'))
        hand.add_card(Card('Spades','Q'))
        hand.add_card(Card('Diamonds','K'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_straight(),True) 
        print('has straight successful')

    def test_flush(self):
        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','3'))
        hand.add_card(Card('Spades','4'))
        hand.add_card(Card('Diamonds','5'))
        hand.add_card(Card('Spades','A'))
        self.assertEqual(hand.has_flush(),False)
        print('no flush successful')
        hand.clear()

        hand.add_card(Card('Hearts','10'))
        hand.add_card(Card('Hearts','J'))
        hand.add_card(Card('Hearts','Q'))
        hand.add_card(Card('Hearts','K'))
        hand.add_card(Card('Hearts','A'))
        self.assertEqual(hand.has_flush(),True) 
        print('has flush successful')

    def test_full_house(self):
        hand = Hand()
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','2'))
        hand.add_card(Card('Diamonds','3'))
        hand.add_card(Card('Spades','3'))
        self.assertEqual(hand.has_full_house(),True)
        print('fullhouse successful')
        hand.clear()

        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','2'))
        hand.add_card(Card('Diamonds','3'))
        hand.add_card(Card('Spades','4'))
        self.assertEqual(hand.has_full_house(),False) 
        print('no fullhouse successful')
        hand.clear()

        hand.add_card(Card('Hearts','A'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','2'))
        hand.add_card(Card('Diamonds','3'))
        hand.add_card(Card('Spades','3'))
        self.assertEqual(hand.has_full_house(),False) 
        print('no fullhouse successful')  

    def test_straight_flush(self):
        hand = Hand()
        hand.add_card(Card('Hearts','A'))
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Hearts','3'))
        hand.add_card(Card('Hearts','4'))
        hand.add_card(Card('Hearts','5'))
        self.assertEqual(hand.has_straight_flush(),True)
        print('straight flush successful')
        hand.clear()

        hand.add_card(Card('Hearts','A'))
        hand.add_card(Card('Clubs','2'))
        hand.add_card(Card('Spades','3'))
        hand.add_card(Card('Diamonds','4'))
        hand.add_card(Card('Spades','5'))
        self.assertEqual(hand.has_straight_flush(),False) 
        print('no straight flush successful')
        hand.clear()

        hand.add_card(Card('Hearts','6'))
        hand.add_card(Card('Hearts','2'))
        hand.add_card(Card('Hearts','3'))
        hand.add_card(Card('Hearts','4'))
        hand.add_card(Card('Hearts','5'))
        self.assertEqual(hand.has_straight_flush(),True)
        print('straight flush successful')
        hand.clear() 


if __name__ == "__main__":
    unittest.main() 