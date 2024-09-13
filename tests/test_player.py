import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from classes.player import Player
from classes.deck import Deck

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestPlayer")
        self.deck = Deck()

    def test_player_has_name(self):
        self.assertEqual(self.player.name, "TestPlayer")

    def test_draw_card(self):
        initial_deck_size = len(self.deck.cards)
        self.player.draw_card(self.deck)
        self.assertEqual(len(self.player.hand), 1)
        self.assertEqual(len(self.deck.cards), initial_deck_size - 1)

if __name__ == '__main__':
    unittest.main()
