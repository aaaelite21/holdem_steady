import unittest

from src.deck import Card
from ..src.holdem import TexasHoldem
# Your test cases will go here
class TestHoldem(unittest.TestCase):

    def setUp(self):
        self.game = TexasHoldem(["Alice", "Bob", "Carol", "David"])

    def test_holdem(self):
        hand_1 = self.game.rank_hand(Card.from_strings(["2H", "3D", "4C", "5S", "6H", "QH", "AS", "AS"]))
        hand_2 = self.game.rank_hand(Card.from_strings(["2H", "3D", "4C", "5S", "6H", "QH", "AS", "AS"]))

if __name__ == '__main__':
    unittest.main()
