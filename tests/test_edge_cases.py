import unittest

from src.hand import Hand, PokerScore, PokerHands

# Your test cases will go here
class TestHoldemEdgeCases(unittest.TestCase):

    def test_one_pair(self):
        common_cards = ["9D", "4H", "7S", "8C", "TD"]
        hand_1 = Hand.from_strings(["AS", "2C"] + common_cards)
        hand_2 = Hand.from_strings(["KS", "QC"] + common_cards)
        assert hand_1 > hand_2, "Ace did not beat vs King"

if __name__ == '__main__':
    unittest.main()